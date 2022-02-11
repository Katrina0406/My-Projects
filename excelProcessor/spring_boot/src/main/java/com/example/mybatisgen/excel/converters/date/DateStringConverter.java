package com.example.mybatisgen.excel.converters.date;

import com.example.mybatisgen.excel.converters.Converter;
import com.example.mybatisgen.excel.enums.CellDataTypeEnum;
import com.example.mybatisgen.excel.metadata.CellData;
import com.example.mybatisgen.excel.metadata.GlobalConfiguration;
import com.example.mybatisgen.excel.metadata.property.ExcelContentProperty;
import com.example.mybatisgen.excel.util.DateUtils;

import java.text.ParseException;
import java.util.Date;

/**
 * Date and string converter
 *
 * @author Jiaju Zhuang
 */
public class DateStringConverter implements Converter<Date> {
    @Override
    public Class supportJavaTypeKey() {
        return Date.class;
    }

    @Override
    public CellDataTypeEnum supportExcelTypeKey() {
        return CellDataTypeEnum.STRING;
    }

    @Override
    public Date convertToJavaData(CellData cellData, ExcelContentProperty contentProperty,
                                  GlobalConfiguration globalConfiguration) throws ParseException {
        if (contentProperty == null || contentProperty.getDateTimeFormatProperty() == null) {
            return DateUtils.parseDate(cellData.getStringValue(), null);
        } else {
            return DateUtils.parseDate(cellData.getStringValue(),
                    contentProperty.getDateTimeFormatProperty().getFormat());
        }
    }

    @Override
    public CellData convertToExcelData(Date value, ExcelContentProperty contentProperty,
                                       GlobalConfiguration globalConfiguration) {
        if (contentProperty == null || contentProperty.getDateTimeFormatProperty() == null) {
            return new CellData(DateUtils.format(value, null));
        } else {
            return new CellData(DateUtils.format(value, contentProperty.getDateTimeFormatProperty().getFormat()));
        }
    }
}
