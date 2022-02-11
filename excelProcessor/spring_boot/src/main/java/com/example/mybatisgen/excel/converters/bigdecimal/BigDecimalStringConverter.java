package com.example.mybatisgen.excel.converters.bigdecimal;

import java.math.BigDecimal;
import java.text.ParseException;

import com.example.mybatisgen.excel.converters.Converter;
import com.example.mybatisgen.excel.enums.CellDataTypeEnum;
import com.example.mybatisgen.excel.metadata.CellData;
import com.example.mybatisgen.excel.metadata.GlobalConfiguration;
import com.example.mybatisgen.excel.metadata.property.ExcelContentProperty;
import com.example.mybatisgen.excel.util.NumberUtils;

/**
 * BigDecimal and string converter
 *
 * @author Jiaju Zhuang
 */
public class BigDecimalStringConverter implements Converter<BigDecimal> {

    @Override
    public Class supportJavaTypeKey() {
        return BigDecimal.class;
    }

    @Override
    public CellDataTypeEnum supportExcelTypeKey() {
        return CellDataTypeEnum.STRING;
    }

    @Override
    public BigDecimal convertToJavaData(CellData cellData, ExcelContentProperty contentProperty,
                                        GlobalConfiguration globalConfiguration) throws ParseException {
        return NumberUtils.parseBigDecimal(cellData.getStringValue(), contentProperty);
    }

    @Override
    public CellData convertToExcelData(BigDecimal value, ExcelContentProperty contentProperty,
                                       GlobalConfiguration globalConfiguration) {
        return NumberUtils.formatToCellData(value, contentProperty);
    }
}
