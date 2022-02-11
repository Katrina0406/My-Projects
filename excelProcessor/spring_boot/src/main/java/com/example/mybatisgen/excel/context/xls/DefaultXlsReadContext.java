package com.example.mybatisgen.excel.context.xls;

import com.example.mybatisgen.excel.context.AnalysisContextImpl;
import com.example.mybatisgen.excel.read.metadata.ReadWorkbook;
import com.example.mybatisgen.excel.read.metadata.holder.xls.XlsReadSheetHolder;
import com.example.mybatisgen.excel.read.metadata.holder.xls.XlsReadWorkbookHolder;
import com.example.mybatisgen.excel.support.ExcelTypeEnum;

/**
 *
 * A context is the main anchorage point of a ls xls reader.
 *
 * @author Jiaju Zhuang
 */
public class DefaultXlsReadContext extends AnalysisContextImpl implements XlsReadContext {

    public DefaultXlsReadContext(ReadWorkbook readWorkbook, ExcelTypeEnum actualExcelType) {
        super(readWorkbook, actualExcelType);
    }

    @Override
    public XlsReadWorkbookHolder xlsReadWorkbookHolder() {
        return (XlsReadWorkbookHolder)readWorkbookHolder();
    }

    @Override
    public XlsReadSheetHolder xlsReadSheetHolder() {
        return (XlsReadSheetHolder)readSheetHolder();
    }
}
