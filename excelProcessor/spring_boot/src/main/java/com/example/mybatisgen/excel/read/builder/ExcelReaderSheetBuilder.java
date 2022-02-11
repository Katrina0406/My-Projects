package com.example.mybatisgen.excel.read.builder;

import com.example.mybatisgen.excel.ExcelReader;
import com.example.mybatisgen.excel.event.SyncReadListener;
import com.example.mybatisgen.excel.exception.ExcelAnalysisException;
import com.example.mybatisgen.excel.exception.ExcelGenerateException;
import com.example.mybatisgen.excel.read.metadata.ReadSheet;

import java.util.List;

/**
 * Build sheet
 *
 * @author Jiaju Zhuang
 */
public class ExcelReaderSheetBuilder extends AbstractExcelReaderParameterBuilder<ExcelReaderSheetBuilder, ReadSheet> {
    private ExcelReader excelReader;
    /**
     * Sheet
     */
    private ReadSheet readSheet;

    public ExcelReaderSheetBuilder() {
        this.readSheet = new ReadSheet();
    }

    public ExcelReaderSheetBuilder(ExcelReader excelReader) {
        this.readSheet = new ReadSheet();
        this.excelReader = excelReader;
    }

    /**
     * Starting from 0
     *
     * @param sheetNo
     * @return
     */
    public ExcelReaderSheetBuilder sheetNo(Integer sheetNo) {
        readSheet.setSheetNo(sheetNo);
        return this;
    }

    /**
     * sheet name
     *
     * @param sheetName
     * @return
     */
    public ExcelReaderSheetBuilder sheetName(String sheetName) {
        readSheet.setSheetName(sheetName);
        return this;
    }

    public ReadSheet build() {
        return readSheet;
    }

    /**
     * Sax read
     */
    public void doRead() {
        if (excelReader == null) {
            throw new ExcelGenerateException("Must use 'EasyExcelFactory.read().sheet()' to call this method");
        }
        excelReader.read(build());
        excelReader.finish();
    }

    /**
     * Synchronous reads return results
     *
     * @return
     */
    public <T> List<T> doReadSync() {
        if (excelReader == null) {
            throw new ExcelAnalysisException("Must use 'EasyExcelFactory.read().sheet()' to call this method");
        }
        SyncReadListener syncReadListener = new SyncReadListener();
        registerReadListener(syncReadListener);
        excelReader.read(build());
        excelReader.finish();
        return (List<T>)syncReadListener.getList();
    }

    @Override
    protected ReadSheet parameter() {
        return readSheet;
    }
}
