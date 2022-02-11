package com.example.mybatisgen.excel.converters.bigdecimal;

import java.math.BigDecimal;

import com.example.mybatisgen.excel.converters.Converter;
import com.example.mybatisgen.excel.enums.CellDataTypeEnum;
import com.example.mybatisgen.excel.metadata.CellData;
import com.example.mybatisgen.excel.metadata.GlobalConfiguration;
import com.example.mybatisgen.excel.metadata.property.ExcelContentProperty;

/**
 * BigDecimal and number converter
 *
 * @author Jiaju Zhuang
 */
public class BigDecimalNumberConverter implements Converter<BigDecimal> {

    @Override
    public Class supportJavaTypeKey() {
        return BigDecimal.class;
    }

    @Override
    public CellDataTypeEnum supportExcelTypeKey() {
        return CellDataTypeEnum.NUMBER;
    }

    @Override
    public BigDecimal convertToJavaData(CellData cellData, ExcelContentProperty contentProperty,
                                        GlobalConfiguration globalConfiguration) {
        return cellData.getNumberValue();
    }

    @Override
    public CellData convertToExcelData(BigDecimal value, ExcelContentProperty contentProperty,
                                       GlobalConfiguration globalConfiguration) {
        return new CellData(value);
    }
}

