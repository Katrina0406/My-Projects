package com.example.mybatisgen.excel.write.handler;

import com.example.mybatisgen.excel.write.metadata.holder.WriteSheetHolder;
import com.example.mybatisgen.excel.write.metadata.holder.WriteWorkbookHolder;

/**
 * intercepts handle sheet creation
 *
 * @author Jiaju Zhuang
 */
public interface SheetWriteHandler extends WriteHandler {

    /**
     * Called before create the sheet
     *
     * @param writeWorkbookHolder
     * @param writeSheetHolder
     */
    void beforeSheetCreate(WriteWorkbookHolder writeWorkbookHolder, WriteSheetHolder writeSheetHolder);

    /**
     * Called after the sheet is created
     *
     * @param writeWorkbookHolder
     * @param writeSheetHolder
     */
    void afterSheetCreate(WriteWorkbookHolder writeWorkbookHolder, WriteSheetHolder writeSheetHolder);
}

