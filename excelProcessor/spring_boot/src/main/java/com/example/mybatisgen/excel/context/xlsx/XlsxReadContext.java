package com.example.mybatisgen.excel.context.xlsx;

import com.example.mybatisgen.excel.context.AnalysisContext;
import com.example.mybatisgen.excel.read.metadata.holder.xlsx.XlsxReadSheetHolder;
import com.example.mybatisgen.excel.read.metadata.holder.xlsx.XlsxReadWorkbookHolder;

/**
 * A context is the main anchorage point of a ls xlsx reader.
 *
 * @author Jiaju Zhuang
 **/
public interface XlsxReadContext extends AnalysisContext {
    /**
     * All information about the workbook you are currently working on.
     *
     * @return Current workbook holder
     */
    XlsxReadWorkbookHolder xlsxReadWorkbookHolder();

    /**
     * All information about the sheet you are currently working on.
     *
     * @return Current sheet holder
     */
    XlsxReadSheetHolder xlsxReadSheetHolder();
}
