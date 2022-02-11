package com.example.mybatisgen.excel.converters.inputstream;

import com.example.mybatisgen.excel.converters.Converter;
import com.example.mybatisgen.excel.enums.CellDataTypeEnum;
import com.example.mybatisgen.excel.metadata.CellData;
import com.example.mybatisgen.excel.metadata.GlobalConfiguration;
import com.example.mybatisgen.excel.metadata.property.ExcelContentProperty;
import com.example.mybatisgen.excel.util.IoUtils;

import java.io.IOException;
import java.io.InputStream;

/**
 * File and image converter
 *
 * @author Jiaju Zhuang
 */
public class InputStreamImageConverter implements Converter<InputStream> {
    @Override
    public Class supportJavaTypeKey() {
        return InputStream.class;
    }

    @Override
    public CellDataTypeEnum supportExcelTypeKey() {
        return CellDataTypeEnum.IMAGE;
    }

    @Override
    public InputStream convertToJavaData(CellData cellData, ExcelContentProperty contentProperty,
                                         GlobalConfiguration globalConfiguration) {
        throw new UnsupportedOperationException("Cannot convert images to input stream");
    }

    @Override
    public CellData convertToExcelData(InputStream value, ExcelContentProperty contentProperty,
                                       GlobalConfiguration globalConfiguration) throws IOException {
        return new CellData(IoUtils.toByteArray(value));
    }

}
