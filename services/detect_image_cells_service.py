from pathlib import Path
from typing import List, Tuple

import cv2
import numpy as np
import itertools

from models.cell import Cell


class DetectImageCellsService:
    @staticmethod
    def call(image_path: Path) -> list[Cell]:
        return DetectImageCellsService(image_path)._detect_cells()

    def __init__(self, image_path: Path | None = None):
        self.image_path = image_path

    def _adaptive_bin(self, gray: np.ndarray) -> np.ndarray:
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        return cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 35, 10
        )

    def _extract_line_masks(self, bw: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        h, w = bw.shape[:2]
        hk = cv2.getStructuringElement(cv2.MORPH_RECT, (max(10, w // 60), 1))
        vk = cv2.getStructuringElement(cv2.MORPH_RECT, (1, max(10, h // 60)))
        h_lines = cv2.morphologyEx(bw, cv2.MORPH_OPEN, hk, iterations=2)
        v_lines = cv2.morphologyEx(bw, cv2.MORPH_OPEN, vk, iterations=2)
        return h_lines, v_lines

    def _hough_positions(self, mask: np.ndarray, vertical: bool) -> List[int]:
        lines = cv2.HoughLinesP(
            mask,
            1,
            np.pi / 180,
            threshold=80,
            minLineLength=min(mask.shape) // 6,
            maxLineGap=10,
        )
        if lines is None:
            return []
        vals = []
        for x1, y1, x2, y2 in lines[:, 0]:
            if vertical and abs(x1 - x2) < 4:
                vals.append(int((x1 + x2) // 2))
            if not vertical and abs(y1 - y2) < 4:
                vals.append(int((y1 + y2) // 2))
        return vals

    def _proj_scan(
        self, mask: np.ndarray, axis: int, group_gap: int = 6, ratio: float = 0.55
    ) -> List[int]:
        proj = np.mean(mask, axis=axis).astype(np.float32)
        proj = cv2.GaussianBlur(proj, (0, 0), sigmaX=3)
        thr = max(1.0, proj.max() * ratio)
        idxs = np.where(proj > thr)[0]
        groups, cur = [], []
        for i in idxs:
            if not cur or i - cur[-1] <= group_gap:
                cur.append(i)
            else:
                groups.append(cur)
                cur = [i]
        if cur:
            groups.append(cur)
        return [int(round(np.mean(g))) for g in groups]

    def _dedupe(self, vals: List[int], tol: int = 10) -> List[int]:
        out = []
        for v in sorted(vals):
            if not out or abs(v - out[-1]) >= tol:
                out.append(v)
            else:
                out[-1] = int(round((out[-1] + v) / 2))
        return out

    def _choose_n_lines(self, cands: List[int], n: int) -> List[int]:
        """Pick n positions that are most evenly spaced."""
        if len(cands) <= n:
            return sorted(cands)
        best = None
        # pyrefly: ignore  # bad-assignment
        for combo in itertools.combinations(sorted(cands), n):
            gaps = np.diff(combo)
            score = np.std(gaps) / (np.mean(gaps) + 1e-6)  # lower is better
            if best is None or score < best[0]:
                best = (score, combo)
        # pyrefly: ignore  # unsupported-operation
        return list(best[1])

    def _detect_cells(self) -> list[Cell]:
        # pyrefly: ignore  # no-matching-overload
        img = cv2.imread(self.image_path)

        if img is None:
            raise FileNotFoundError("Image not found or unreadable")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        bw = self._adaptive_bin(gray)
        h_mask, v_mask = self._extract_line_masks(bw)

        x_c = self._dedupe(self._hough_positions(v_mask, True), 8)
        y_c = self._dedupe(self._hough_positions(h_mask, False), 8)

        expected_lines = 6
        if len(x_c) < expected_lines:
            x_c = self._proj_scan(v_mask, axis=0)

        if len(y_c) < expected_lines:
            y_c = self._proj_scan(h_mask, axis=1)

        x_c = self._dedupe(x_c, 10)
        y_c = self._dedupe(y_c, 10)

        grid = cv2.bitwise_or(h_mask, v_mask)
        # pyrefly: ignore  # no-matching-overload
        grid = cv2.dilate(grid, np.ones((3, 3), np.uint8), 1)
        nz = cv2.findNonZero(grid)
        x, y, w, h = cv2.boundingRect(nz)
        x_c = [v for v in x_c if x - 5 <= v <= x + w + 5]
        y_c = [v for v in y_c if y - 5 <= v <= y + h + 5]

        xs = self._choose_n_lines(x_c, expected_lines)
        ys = self._choose_n_lines(y_c, expected_lines)
        xs.sort()
        ys.sort()

        cells: List[Cell] = []
        for r in range(len(ys) - 1):
            for c in range(len(xs) - 1):
                cells.append(Cell(r, c, xs[c], ys[r], xs[c + 1], ys[r + 1]))

        return cells

    def draw_grid_overlay(self, image_path: str, output_path: str = "overlay.png"):
        cells = self._detect_cells()

        img = cv2.imread(image_path)
        # pyrefly: ignore  # missing-attribute
        overlay = img.copy()

        for c in cells:
            cv2.rectangle(overlay, (c.x1, c.y1), (c.x2, c.y2), (0, 0, 255), 1)
            label = f"{c.row},{c.col}"
            cv2.putText(
                overlay,
                label,
                (c.x1 + 5, c.y1 + 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1,
            )

        cv2.imwrite(output_path, overlay)
