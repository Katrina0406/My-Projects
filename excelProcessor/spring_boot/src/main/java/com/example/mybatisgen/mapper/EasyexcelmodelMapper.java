package com.example.mybatisgen.mapper;

import com.example.mybatisgen.entity.Easyexcelmodel;
import com.example.mybatisgen.entity.EasyexcelmodelExample;
import org.apache.ibatis.annotations.Param;

import java.util.List;

public interface EasyexcelmodelMapper {
    int countByExample(EasyexcelmodelExample example);

    int deleteByExample(EasyexcelmodelExample example);

    int deleteByPrimaryKey(Integer id);

    int insert(Easyexcelmodel record);

    int insertSelective(Easyexcelmodel record);

    List<Easyexcelmodel> selectByExample(EasyexcelmodelExample example);

    Easyexcelmodel selectByPrimaryKey(Integer id);

    int updateByExampleSelective(@Param("record") Easyexcelmodel record, @Param("example") EasyexcelmodelExample example);

    int updateByExample(@Param("record") Easyexcelmodel record, @Param("example") EasyexcelmodelExample example);

    int updateByPrimaryKeySelective(Easyexcelmodel record);

    int updateByPrimaryKey(Easyexcelmodel record);
}