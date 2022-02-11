package com.example.mybatisgen.excel.converters.longconverter;

import com.example.mybatisgen.excel.converters.Converter;
import com.example.mybatisgen.excel.enums.CellDataTypeEnum;
import com.example.mybatisgen.excel.metadata.CellData;
import com.example.mybatisgen.excel.metadata.GlobalConfiguration;
import com.example.mybatisgen.excel.metadata.property.ExcelContentProperty;

import java.math.BigDecimal;

/**
 * Long and number converter
 *
 * @author Jiaju Zhuang
 */
public class LongNumberConverter implements Converter<Long> {

    @Override
    public Class supportJavaTypeKey() {
        return Long.class;
    }

    @Override
    public CellDataTypeEnum supportExcelTypeKey() {
        return CellDataTypeEnum.NUMBER;
    }

    @Override
    public Long convertToJavaData(CellData cellData, ExcelContentProperty contentProperty,
                                  GlobalConfiguration globalConfiguration) {
        return cellData.getNumberValue().longValue();
    }

    @Override
    public CellData convertToExcelData(Long value, ExcelContentProperty contentProperty,
                                       GlobalConfiguration globalConfiguration) {
        return new CellData(BigDecimal.valueOf(value));
    }

}
