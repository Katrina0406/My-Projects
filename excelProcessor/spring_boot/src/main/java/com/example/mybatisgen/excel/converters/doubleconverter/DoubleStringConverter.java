package com.example.mybatisgen.excel.converters.doubleconverter;

import com.example.mybatisgen.excel.converters.Converter;
import com.example.mybatisgen.excel.enums.CellDataTypeEnum;
import com.example.mybatisgen.excel.metadata.CellData;
import com.example.mybatisgen.excel.metadata.GlobalConfiguration;
import com.example.mybatisgen.excel.metadata.property.ExcelContentProperty;
import com.example.mybatisgen.excel.util.NumberUtils;

import java.text.ParseException;

/**
 * Double and string converter
 *
 * @author Jiaju Zhuang
 */
public class DoubleStringConverter implements Converter<Double> {

    @Override
    public Class supportJavaTypeKey() {
        return Double.class;
    }

    @Override
    public CellDataTypeEnum supportExcelTypeKey() {
        return CellDataTypeEnum.STRING;
    }

    @Override
    public Double convertToJavaData(CellData cellData, ExcelContentProperty contentProperty,
                                    GlobalConfiguration globalConfiguration) throws ParseException {
        return NumberUtils.parseDouble(cellData.getStringValue(), contentProperty);
    }

    @Override
    public CellData convertToExcelData(Double value, ExcelContentProperty contentProperty,
                                       GlobalConfiguration globalConfiguration) {
        return NumberUtils.formatToCellData(value, contentProperty);
    }
}
