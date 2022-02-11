package com.example.mybatisgen.excel.converters.integer;

import com.example.mybatisgen.excel.converters.Converter;
import com.example.mybatisgen.excel.enums.CellDataTypeEnum;
import com.example.mybatisgen.excel.metadata.CellData;
import com.example.mybatisgen.excel.metadata.GlobalConfiguration;
import com.example.mybatisgen.excel.metadata.property.ExcelContentProperty;

import java.math.BigDecimal;

/**
 * Integer and number converter
 *
 * @author Jiaju Zhuang
 */
public class IntegerNumberConverter implements Converter<Integer> {

    @Override
    public Class supportJavaTypeKey() {
        return Integer.class;
    }

    @Override
    public CellDataTypeEnum supportExcelTypeKey() {
        return CellDataTypeEnum.NUMBER;
    }

    @Override
    public Integer convertToJavaData(CellData cellData, ExcelContentProperty contentProperty,
                                     GlobalConfiguration globalConfiguration) {
        return cellData.getNumberValue().intValue();
    }

    @Override
    public CellData convertToExcelData(Integer value, ExcelContentProperty contentProperty,
                                       GlobalConfiguration globalConfiguration) {
        return new CellData(new BigDecimal(Integer.toString(value)));
    }

}
