package com.example.mybatisgen.excel.converters.byteconverter;

import com.example.mybatisgen.excel.converters.Converter;
import com.example.mybatisgen.excel.enums.CellDataTypeEnum;
import com.example.mybatisgen.excel.metadata.CellData;
import com.example.mybatisgen.excel.metadata.GlobalConfiguration;
import com.example.mybatisgen.excel.metadata.property.ExcelContentProperty;

import java.math.BigDecimal;

/**
 * Byte and number converter
 *
 * @author Jiaju Zhuang
 */
public class ByteNumberConverter implements Converter<Byte> {

    @Override
    public Class supportJavaTypeKey() {
        return Byte.class;
    }

    @Override
    public CellDataTypeEnum supportExcelTypeKey() {
        return CellDataTypeEnum.NUMBER;
    }

    @Override
    public Byte convertToJavaData(CellData cellData, ExcelContentProperty contentProperty,
                                  GlobalConfiguration globalConfiguration) {
        return cellData.getNumberValue().byteValue();
    }

    @Override
    public CellData convertToExcelData(Byte value, ExcelContentProperty contentProperty,
                                       GlobalConfiguration globalConfiguration) {
        return new CellData(new BigDecimal(Byte.toString(value)));
    }

}
