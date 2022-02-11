package com.example.mybatisgen.excel.analysis.v03.handlers;

import com.example.mybatisgen.excel.analysis.v03.IgnorableXlsRecordHandler;
import com.example.mybatisgen.excel.constant.BuiltinFormats;
import com.example.mybatisgen.excel.context.xls.XlsReadContext;
import com.example.mybatisgen.excel.enums.CellDataTypeEnum;
import com.example.mybatisgen.excel.enums.RowTypeEnum;
import com.example.mybatisgen.excel.metadata.Cell;
import com.example.mybatisgen.excel.metadata.CellData;
import org.apache.poi.hssf.model.HSSFFormulaParser;
import org.apache.poi.hssf.record.FormulaRecord;
import org.apache.poi.hssf.record.Record;
import org.apache.poi.ss.usermodel.CellType;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.math.BigDecimal;
import java.util.Map;

/**
 * Record handler
 *
 * @author Dan Zheng
 */
public class FormulaRecordHandler extends AbstractXlsRecordHandler implements IgnorableXlsRecordHandler {
    private static final Logger LOGGER = LoggerFactory.getLogger(FormulaRecordHandler.class);
    private static final String ERROR = "#VALUE!";

    @Override
    public void processRecord(XlsReadContext xlsReadContext, Record record) {
        FormulaRecord frec = (FormulaRecord)record;
        Map<Integer, Cell> cellMap = xlsReadContext.xlsReadSheetHolder().getCellMap();
        CellData tempCellData = new CellData();
        tempCellData.setRowIndex(frec.getRow());
        tempCellData.setColumnIndex((int)frec.getColumn());
        CellType cellType = CellType.forInt(frec.getCachedResultType());
        String formulaValue = null;
        try {
            formulaValue = HSSFFormulaParser.toFormulaString(xlsReadContext.xlsReadWorkbookHolder().getHssfWorkbook(),
                    frec.getParsedExpression());
        } catch (Exception e) {
            LOGGER.debug("Get formula value error.", e);
        }
        tempCellData.setFormula(Boolean.TRUE);
        tempCellData.setFormulaValue(formulaValue);
        xlsReadContext.xlsReadSheetHolder().setTempRowType(RowTypeEnum.DATA);
        switch (cellType) {
            case STRING:
                // Formula result is a string
                // This is stored in the next record
                tempCellData.setType(CellDataTypeEnum.STRING);
                xlsReadContext.xlsReadSheetHolder().setTempCellData(tempCellData);
                break;
            case NUMERIC:
                tempCellData.setType(CellDataTypeEnum.NUMBER);
                tempCellData.setNumberValue(BigDecimal.valueOf(frec.getValue()));
                Integer dataFormat =
                        xlsReadContext.xlsReadWorkbookHolder().getFormatTrackingHSSFListener().getFormatIndex(frec);
                tempCellData.setDataFormat(dataFormat);
                tempCellData.setDataFormatString(BuiltinFormats.getBuiltinFormat(dataFormat,
                        xlsReadContext.xlsReadWorkbookHolder().getFormatTrackingHSSFListener().getFormatString(frec),
                        xlsReadContext.readSheetHolder().getGlobalConfiguration().getLocale()));
                cellMap.put((int)frec.getColumn(), tempCellData);
                break;
            case ERROR:
                tempCellData.setType(CellDataTypeEnum.ERROR);
                tempCellData.setStringValue(ERROR);
                cellMap.put((int)frec.getColumn(), tempCellData);
                break;
            case BOOLEAN:
                tempCellData.setType(CellDataTypeEnum.BOOLEAN);
                tempCellData.setBooleanValue(frec.getCachedBooleanValue());
                cellMap.put((int)frec.getColumn(), tempCellData);
                break;
            default:
                tempCellData.setType(CellDataTypeEnum.EMPTY);
                cellMap.put((int)frec.getColumn(), tempCellData);
                break;
        }
    }
}
