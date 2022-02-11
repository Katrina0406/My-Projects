package com.example.mybatisgen.excel.converters.file;

import com.example.mybatisgen.excel.converters.Converter;
import com.example.mybatisgen.excel.enums.CellDataTypeEnum;
import com.example.mybatisgen.excel.metadata.CellData;
import com.example.mybatisgen.excel.metadata.GlobalConfiguration;
import com.example.mybatisgen.excel.metadata.property.ExcelContentProperty;
import com.example.mybatisgen.excel.util.FileUtils;

import java.io.File;
import java.io.IOException;

/**
 * File and image converter
 *
 * @author Jiaju Zhuang
 */
public class FileImageConverter implements Converter<File> {
    @Override
    public Class supportJavaTypeKey() {
        return File.class;
    }

    @Override
    public CellDataTypeEnum supportExcelTypeKey() {
        return CellDataTypeEnum.IMAGE;
    }

    @Override
    public File convertToJavaData(CellData cellData, ExcelContentProperty contentProperty,
                                  GlobalConfiguration globalConfiguration) {
        throw new UnsupportedOperationException("Cannot convert images to file");
    }

    @Override
    public CellData convertToExcelData(File value, ExcelContentProperty contentProperty,
                                       GlobalConfiguration globalConfiguration) throws IOException {
        return new CellData(FileUtils.readFileToByteArray(value));
    }

}

