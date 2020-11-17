*** Settings ***
Resource       ../apis/fuelcard_api.robot
Resource       ../apis/longtengserver_db.robot


*** Test Cases ***
测试正常添加加油卡
    [Documentation]     添加新卡并返回添加成功
    ${res}              添加加油卡            hzc_00001
    STATUS SHOULD BE    200                 ${res}
    ${res_dict}         Set Variable        ${res.json()}
#    SHOULD BE EQUAL     添加卡成功            ${res_dict['msg']}
    Should not Be True     ${res_dict['success']}
    ${check_result}     数据库检查卡是否存在    hzc_00001
    Log to console      ${check_result}


