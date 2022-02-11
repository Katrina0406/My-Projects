package com.example.mybatisgen.excel.converters.shortconverter;

import com.example.mybatisgen.excel.converters.Converter;
import com.example.mybatisgen.excel.enums.CellDataTypeEnum;
import com.example.mybatisgen.excel.metadata.CellData;
import com.example.mybatisgen.excel.metadata.GlobalConfiguration;
import com.example.mybatisgen.excel.metadata.property.ExcelContentProperty;

import java.math.BigDecimal;

/**
 * Short and number converter
 *
 * @author Jiaju Zhuang
 */
public class ShortNumberConverter implements Converter<Short> {

    @Override
    public Class supportJavaTypeKey() {
        return Short.class;
    }

    @Override
    public CellDataTypeEnum supportExcelTypeKey() {
        return CellDataTypeEnum.NUMBER;
    }

    @Override
    public Short convertToJavaData(CellData cellData, ExcelContentProperty contentProperty,
                                   GlobalConfiguration globalConfiguration) {
        return cellData.getNumberValue().shortValue();
    }

    @Override
    public CellData convertToExcelData(Short value, ExcelContentProperty contentProperty,
                                       GlobalConfiguration globalConfiguration) {
        return new CellData(new BigDecimal(Short.toString(value)));
    }

}