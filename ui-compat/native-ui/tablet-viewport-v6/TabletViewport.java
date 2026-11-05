package org.tb371fc.layout;

import com.android.launcher.layoutparam.ConfigParam;
import com.android.launcher.layoutparam.WorkspaceParam;

public final class TabletViewport {
    private TabletViewport() {}

    private static boolean applies(ConfigParam config) {
        int width = config.getWidthPx();
        int height = config.getHeightPx();
        return config.isTablet() && !config.isTwoPanels() && !config.isMultiWindowMode()
                && Math.min(width, height) == 1840 && Math.max(width, height) == 2944;
    }

    public static int cellHeight(int original, int viewportMaximum, WorkspaceParam workspace, int columns, int rows) {
        ConfigParam config = workspace.getMConfig();
        if (!applies(config) || viewportMaximum <= 0 || viewportMaximum > config.getHeightPx() || rows != config.getNumRows() || columns != config.getNumColumns() || rows <= 0) {
            return Math.min(original, viewportMaximum);
        }
        // The native workspace allocator positions the grid after the cell
        // height is known. Use fixed resource reserves so rebuilds and rotations
        // never feed the preceding layout's padding back into the next one.
        int top = 0;
        if (config.getWidthPx() < config.getHeightPx()) {
            int resource = config.getRes().getIdentifier("workspace_padding_top_adjustment", "dimen", "com.android.launcher");
            if (resource != 0) {
                top = config.getRes().getDimensionPixelSize(resource);
            }
        }
        int gap = Math.round(8 * config.getRes().getDisplayMetrics().density);
        int available = Math.max(rows, viewportMaximum * rows - top - gap);
        int height = available / rows;
        return config.getWidthPx() < config.getHeightPx() ? height : Math.min(original, height);
    }
}
