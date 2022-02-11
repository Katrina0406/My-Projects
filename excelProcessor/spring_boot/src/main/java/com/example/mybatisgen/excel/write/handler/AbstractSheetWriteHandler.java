package com.example.mybatisgen.excel.write.handler;

import com.example.mybatisgen.excel.write.metadata.holder.WriteSheetHolder;
import com.example.mybatisgen.excel.write.metadata.holder.WriteWorkbookHolder;

/**
 * Abstract sheet write handler
 *
 * @author Jiaju Zhuang
 **/
public abstract class AbstractSheetWriteHandler implements SheetWriteHandler {
    @Override
    public void beforeSheetCreate(WriteWorkbookHolder writeWorkbookHolder, WriteSheetHolder writeSheetHolder) {

    }

    @Override
    public void afterSheetCreate(WriteWorkbookHolder writeWorkbookHolder, WriteSheetHolder writeSheetHolder) {

    }
}
