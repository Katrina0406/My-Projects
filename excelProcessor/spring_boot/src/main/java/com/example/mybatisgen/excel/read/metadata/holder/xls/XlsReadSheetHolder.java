package com.example.mybatisgen.excel.read.metadata.holder.xls;

import java.util.HashMap;
import java.util.Map;

import com.example.mybatisgen.excel.enums.RowTypeEnum;
import com.example.mybatisgen.excel.read.metadata.ReadSheet;
import com.example.mybatisgen.excel.read.metadata.holder.ReadSheetHolder;
import com.example.mybatisgen.excel.read.metadata.holder.ReadWorkbookHolder;

/**
 * sheet holder
 *
 * @author Jiaju Zhuang
 */
public class XlsReadSheetHolder extends ReadSheetHolder {
    /**
     * Row type.Temporary storage, last set in <code>ReadRowHolder</code>.
     */
    private RowTypeEnum tempRowType;
    /**
     * Temp object index.
     */
    private Integer tempObjectIndex;
    /**
     * Temp object index.
     */
    private Map<Integer, String> objectCacheMap;

    public XlsReadSheetHolder(ReadSheet readSheet, ReadWorkbookHolder readWorkbookHolder) {
        super(readSheet, readWorkbookHolder);
        tempRowType = RowTypeEnum.EMPTY;
        objectCacheMap = new HashMap<Integer, String>(16);
    }

    public RowTypeEnum getTempRowType() {
        return tempRowType;
    }

    public void setTempRowType(RowTypeEnum tempRowType) {
        this.tempRowType = tempRowType;
    }


    public Integer getTempObjectIndex() {
        return tempObjectIndex;
    }

    public void setTempObjectIndex(Integer tempObjectIndex) {
        this.tempObjectIndex = tempObjectIndex;
    }

    public Map<Integer, String> getObjectCacheMap() {
        return objectCacheMap;
    }

    public void setObjectCacheMap(Map<Integer, String> objectCacheMap) {
        this.objectCacheMap = objectCacheMap;
    }
}