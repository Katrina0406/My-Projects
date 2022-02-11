package com.example.mybatisgen.excel.converters.string;

import com.example.mybatisgen.excel.converters.Converter;
import com.example.mybatisgen.excel.enums.CellDataTypeEnum;
import com.example.mybatisgen.excel.metadata.CellData;
import com.example.mybatisgen.excel.metadata.GlobalConfiguration;
import com.example.mybatisgen.excel.metadata.property.ExcelContentProperty;
import com.example.mybatisgen.excel.util.DateUtils;
import com.example.mybatisgen.excel.util.NumberDataFormatterUtils;
import com.example.mybatisgen.excel.util.NumberUtils;
import com.example.mybatisgen.excel.util.StringUtils;
import org.apache.poi.ss.usermodel.DateUtil;

import java.math.BigDecimal;

/**
 * String and number converter
 *
 * @author Jiaju Zhuang
 */
public class StringNumberConverter implements Converter<String> {

    @Override
    public Class supportJavaTypeKey() {
        return String.class;
    }

    @Override
    public CellDataTypeEnum supportExcelTypeKey() {
        return CellDataTypeEnum.NUMBER;
    }

    @Override
    public String convertToJavaData(CellData cellData, ExcelContentProperty contentProperty,
                                    GlobalConfiguration globalConfiguration) {
        // If there are "DateTimeFormat", read as date
        if (contentProperty != null && contentProperty.getDateTimeFormatProperty() != null) {
            return DateUtils.format(
                    DateUtil.getJavaDate(cellData.getNumberValue().doubleValue(),
                            contentProperty.getDateTimeFormatProperty().getUse1904windowing(), null),
                    contentProperty.getDateTimeFormatProperty().getFormat());
        }
        // If there are "NumberFormat", read as number
        if (contentProperty != null && contentProperty.getNumberFormatProperty() != null) {
            return NumberUtils.format(cellData.getNumberValue(), contentProperty);
        }
        // Excel defines formatting
        if (cellData.getDataFormat() != null && !StringUtils.isEmpty(cellData.getDataFormatString())) {
            return NumberDataFormatterUtils.format(cellData.getNumberValue(), cellData.getDataFormat(),
                    cellData.getDataFormatString(), globalConfiguration);
        }
        // Default conversion number
        return NumberUtils.format(cellData.getNumberValue(), contentProperty);
    }

    @Override
    public CellData convertToExcelData(String value, ExcelContentProperty contentProperty,
                                       GlobalConfiguration globalConfiguration) {
        return new CellData(new BigDecimal(value));
    }
}
