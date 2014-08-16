#AKBQuiz API说明#
----------

##获取问题接口##

###说明###
API名：**getquiz**   
作用：根据请求返回符合要求的题目列表。  
HTTP请求方式：**GET** 参数为多值的用半角逗号隔开

    http://domain.of.server/quiz/getquiz/?arg1=value1&arg2=value2,value3

###参数###

 - **group**   
   *相关团体*: 要求全称 可以是多个值 不分大小写   
   *默认值*: 所有团体
 - **n**  
   *题目数量*  
   *默认值*: `20`
 - **category**  
   *题目类型*: 可以是设置见下文所述  
   *默认值*: `f` 所有网友出题 
 - **coding**   
   *编码*: 目前只支持UTF-8编码   
   *默认值*: `utf-8`
 - **difficulty**  
   *难度*: 一定是两个值 范围在1~10之间 下限在前 目前不可用  
   *默认值*: `1,10`
 - **format**  
   *格式*: 返回值的包装方式 `xml`和`json`两值可选   
   *默认值*: `json`

> **题目类型`category`参数说明**  
> 目前版本题库中可以生成的问题分类如下：
> 
>  1. 网友出题 `f`(Fun qiuz)   
>  2. 成员信息 `i`(Info quiz)  
>      1) 出生地 `c` (comefrom)   
>      2) 生日 `b` (birthday)  
>      3) 所属队伍 `t` (team)
>  
> 将参数`type`的值设定为其中任意一个或者多个值，可以使返回的题目列表中不包含其他类型的题目。例如：`type=f,b,t`表示只获取网友出题、成员生日和所属队伍的题目。这三种类型的题目比例为1:1:1。  
> 在每个类型之后附上数字可以指定题目的比例，不附数值的项默认为1。例如`type=f6,b,t2`表示这三种类型题目的比例为6:1:2。
> 如果在类型之前附上`u`则表示不要这种类型的题目。例如`type=f6,i,ub`表示网友出题和成员信息题的比例是6:1，但是不要问生日题。这样出生地和所属队伍的题目比例将是1:1

###返回###

返回一个数组，数组内每一个元素中包含题目的信息。

 - **id** 题目的唯一id，只有网友提供的题目才有这个id
 - **q** 问题内容
 - **a** 4个选项的内容
 - **c** 正确答案的下标(0~3)

###示例###
**请求**

    http://domain.of.server/quiz/getquiz/?n=10&group=AKB48,HKT48&difficulty=2,5&format=json&type=f6,i,ub

**返回**  
`json`格式:
    
    [
      {
        "q": "\u672c\u90e8\u54ea\u652f\u961f\u4f0d\u7b2c\u4e00\u6b21\u521d\u65e5\u6ee1\u5458\uff1f", 
        "a": [
          "Team K", 
          "TeamA", 
          "Team 4", 
          "Team B"
        ], 
        "c": 0, 
        "id": 12
      }, 
      ...
    ]

`xml`格式:

    <?xml version='1.0' encoding='UTF-8'?>
    <!DOCTYPE array >
    <array>
      <item>
        <id>65</id>
        <question>TEAM B的double tower是哪两只</question>
        <correctindex>2</correctindex>
        <array>
          <answer>增田有华 北原里英</answer>
          <answer>铃木玛利亚 小森美果</answer>
          <answer>佐藤堇 铃木紫帆里</answer>
          <answer>柏木由纪 渡边麻友</answer>
        </array>
      </item>
      ...
    <array>

----------

##获取成员信息接口##

###说明###
API名：**getinfo**   
作用：根据请求返回符合要求的成员信息。  
HTTP请求方式：**GET** 参数为多值的用半角逗号隔开

###参数###
