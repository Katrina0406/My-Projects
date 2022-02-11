package com.example.mybatisgen.excel.write.merge;

import org.apache.poi.ss.util.CellRangeAddress;

import com.example.mybatisgen.excel.metadata.property.OnceAbsoluteMergeProperty;
import com.example.mybatisgen.excel.write.handler.AbstractSheetWriteHandler;
import com.example.mybatisgen.excel.write.metadata.holder.WriteSheetHolder;
import com.example.mybatisgen.excel.write.metadata.holder.WriteWorkbookHolder;

/**
 * It only merges once when create cell(firstRowIndex,lastRowIndex)
 *
 * @author Jiaju Zhuang
 */
public class OnceAbsoluteMergeStrategy extends AbstractSheetWriteHandler {
    /**
     * First row
     */
    private int firstRowIndex;
    /**
     * Last row
     */
    private int lastRowIndex;
    /**
     * First column
     */
    private int firstColumnIndex;
    /**
     * Last row
     */
    private int lastColumnIndex;

    public OnceAbsoluteMergeStrategy(int firstRowIndex, int lastRowIndex, int firstColumnIndex, int lastColumnIndex) {
        if (firstRowIndex < 0 || lastRowIndex < 0 || firstColumnIndex < 0 || lastColumnIndex < 0) {
            throw new IllegalArgumentException("All parameters must be greater than 0");
        }
        this.firstRowIndex = firstRowIndex;
        this.lastRowIndex = lastRowIndex;
        this.firstColumnIndex = firstColumnIndex;
        this.lastColumnIndex = lastColumnIndex;
    }

    public OnceAbsoluteMergeStrategy(OnceAbsoluteMergeProperty onceAbsoluteMergeProperty) {
        this(onceAbsoluteMergeProperty.getFirstRowIndex(), onceAbsoluteMergeProperty.getLastRowIndex(),
                onceAbsoluteMergeProperty.getFirstColumnIndex(), onceAbsoluteMergeProperty.getLastColumnIndex());
    }

    @Override
    public void afterSheetCreate(WriteWorkbookHolder writeWorkbookHolder, WriteSheetHolder writeSheetHolder) {
        CellRangeAddress cellRangeAddress =
                new CellRangeAddress(firstRowIndex, lastRowIndex, firstColumnIndex, lastColumnIndex);
        writeSheetHolder.getSheet().addMergedRegionUnsafe(cellRangeAddress);
    }
}
