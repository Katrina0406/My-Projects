package com.example.mybatisgen.excel.write.style.column;

import java.util.List;

import org.apache.poi.ss.usermodel.Cell;

import com.example.mybatisgen.excel.event.NotRepeatExecutor;
import com.example.mybatisgen.excel.metadata.CellData;
import com.example.mybatisgen.excel.metadata.Head;
import com.example.mybatisgen.excel.write.handler.AbstractCellWriteHandler;
import com.example.mybatisgen.excel.write.metadata.holder.WriteSheetHolder;
import com.example.mybatisgen.excel.write.metadata.holder.WriteTableHolder;

/**
 * Column width style strategy
 *
 * @author Jiaju Zhuang
 */
public abstract class AbstractColumnWidthStyleStrategy extends AbstractCellWriteHandler implements NotRepeatExecutor {

    @Override
    public String uniqueValue() {
        return "ColumnWidthStyleStrategy";
    }

    @Override
    public void afterCellDispose(WriteSheetHolder writeSheetHolder, WriteTableHolder writeTableHolder,
                                 List<CellData> cellDataList, Cell cell, Head head, Integer relativeRowIndex, Boolean isHead) {
        setColumnWidth(writeSheetHolder, cellDataList, cell, head, relativeRowIndex, isHead);
    }

    /**
     * Sets the column width when head create
     *
     * @param writeSheetHolder
     * @param cellDataList
     * @param cell
     * @param head
     * @param relativeRowIndex
     * @param isHead
     */
    protected abstract void setColumnWidth(WriteSheetHolder writeSheetHolder, List<CellData> cellDataList, Cell cell,
                                           Head head, Integer relativeRowIndex, Boolean isHead);

}

