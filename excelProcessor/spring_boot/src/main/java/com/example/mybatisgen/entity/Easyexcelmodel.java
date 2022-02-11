package com.example.mybatisgen.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import com.example.mybatisgen.excel.annotation.ExcelIgnore;
import com.example.mybatisgen.excel.annotation.ExcelProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

import java.io.Serializable;

@Data
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode
@TableName("EasyExcelModel")
public class Easyexcelmodel implements Serializable {

    @TableId(value = "id", type = IdType.AUTO)
    @ExcelIgnore // 下载的Excel的表头中忽略此字段
    private Integer id;

    @ExcelProperty("姓名") //映射Excel的标题名称
    @TableField("name")  //mybatis-plus 对应的数据库字段名称
    private String name;

    @ExcelProperty("年龄")
    @TableField("age")
    private String age;

    @ExcelProperty("地址")
    @TableField("address")
    private String address;

    private static final long serialVersionUID = 1L;

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name == null ? null : name.trim();
    }

    public String getAge() {
        return age;
    }

    public void setAge(String age) {
        this.age = age == null ? null : age.trim();
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address == null ? null : address.trim();
    }

    @Override
    public String toString() {
        return "Easyexcelmodel{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", age='" + age + '\'' +
                ", address='" + address + '\'' +
                '}';
    }
}