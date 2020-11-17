*** Settings ***
Documentation       加油卡接口
Library             RequestsLibrary

*** Variables ***
${data_source_id}   bHRz
${base_url}         http://115.28.108.130:8080

*** Keywords ***
添加加油卡
    [Arguments]     ${card_number}
    &{card_info}    Create Dictionary   cardNumber=${card_number}
    &{data}         Create Dictionary   dataSourceId=${data_source_id}   methodId=00A            CardInfo=&{card_info}
    CREATE SESSION  session             ${base_url}
    ${res}          POST REQUEST        session          /gasStation/process     json=${data}
    LOG TO CONSOLE          ${res.json()}
    [Return]        ${res}



