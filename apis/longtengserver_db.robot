*** Settings ***
Library         DatabaseLibrary


*** Variables ***
${db_host}          115.28.108.130
${db_name}          longtengserver
${db_user}          test
${db_pwd}           abc123456


*** Keywords ***
查询数据库
    [Arguments]     ${sql}
    connect to database using custom params     pymysql     host='${db_host}',port=3306,user='${db_user}',password='${db_pwd}',db='${db_name}'
    ${result}       query       ${sql}
    Log To Console      ${result}
    disconnect from database
    [Return]      ${result}

数据库检查卡是否存在
    [Arguments]     ${card_number}
    ${sql}          Set Variable        SELECT cardNumber FROM cardInfo WHERE cardNumber="${card_number}"
    ${result}       查询数据库       ${sql}
    ${check_result}       Set Variable If    ${result}     True　　　　False
    [Return]        ${check_result}