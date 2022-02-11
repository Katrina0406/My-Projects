package com.example.mybatisgen.excel.converters.shortconverter;

import com.example.mybatisgen.excel.converters.Converter;
import com.example.mybatisgen.excel.enums.CellDataTypeEnum;
import com.example.mybatisgen.excel.metadata.CellData;
import com.example.mybatisgen.excel.metadata.GlobalConfiguration;
import com.example.mybatisgen.excel.metadata.property.ExcelContentProperty;
import com.example.mybatisgen.excel.util.NumberUtils;

import java.text.ParseException;

/**
 * Short and string converter
 *
 * @author Jiaju Zhuang
 */
public class ShortStringConverter implements Converter<Short> {

    @Override
    public Class supportJavaTypeKey() {
        return Short.class;
    }

    @Override
    public CellDataTypeEnum supportExcelTypeKey() {
        return CellDataTypeEnum.STRING;
    }

    @Override
    public Short convertToJavaData(CellData cellData, ExcelContentProperty contentProperty,
                                   GlobalConfiguration globalConfiguration) throws ParseException {
        return NumberUtils.parseShort(cellData.getStringValue(), contentProperty);
    }

    @Override
    public CellData convertToExcelData(Short value, ExcelContentProperty contentProperty,
                                       GlobalConfiguration globalConfiguration) {
        return NumberUtils.formatToCellData(value, contentProperty);
    }
}