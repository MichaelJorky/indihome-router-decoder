#!/bin/sh
## Rabu,13 Maret 2024
## Script Login Router ZTE F670L
## Modif by Dunia MR



login=admin
password=Telkomdso123
ipont=http://192.168.1.1

##Simpan Cookie
cookie=$(
    curl -s -c cookie.txt ${ipont} \
        -H 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 15_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1' \
        -H 'Cache-Control: max-age=0\r\n' \
        --compressed \
        --insecure
)

#cari seasion token
ses_token_req=$(curl -s -b cookie.txt "${ipont}/?_type=loginData&_tag=login_entry" \
    -H 'Accept: application/json, text/javascript, */*; q=0.01' \
    -H 'Accept-Language: id' \
    -H 'Connection: keep-alive' \
    -H 'DNT: 1' \
    -H 'Referer: ${ipont}/' \
    -H 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 15_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1' \
    -H 'X-Requested-With: XMLHttpRequest' \
    --compressed \
    --insecure)
#sample output {"lockingTime":0,"loginErrMsg":"","promptMsg":"","sess_token":"2449946313382634"}
ses_token=$(echo $ses_token_req | awk -F":" '{print $5}' | grep -o '[0-9]\+')
echo "session token = $ses_token"

#cari password seed <ajax_response_xml_root>59469541</ajax_response_xml_root>
pseed_req=$(curl -s -b cookie.txt "${ipont}/?_type=loginData&_tag=login_token&_="$(date +%s)"" \
    -H 'Accept: application/json, text/javascript, */*; q=0.01' \
    -H 'Accept-Language: id' \
    -H 'Connection: keep-alive' \
    -H 'DNT: 1' \
    -H 'Referer: ${ipont}/' \
    -H 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 15_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1' \
    -H 'X-Requested-With: XMLHttpRequest' \
    --compressed \
    --insecure)

pseed=$(echo $pseed_req | awk -F '[<>]' '/ajax_response_xml_root/{print $3 }')
echo "Password seed = $pseed"

#login request
passenc=$(echo -n $password$pseed | sha256sum | awk '{print $1}')
echo "Encrypted password = $passenc"
login_req=$(curl -s -b cookie.txt -c cookie.txt "${ipont}/?_type=loginData&_tag=login_entry" \
    -H 'Accept: application/json, text/javascript, */*; q=0.01' \
    -H 'Accept-Language: id,en-US;q=0.9,en;q=0.8,gl;q=0.7' \
    -H 'Connection: keep-alive' \
    -H 'DNT: 1' \
    -H 'Referer: ${ipont}/' \
    -H 'Accept-Encoding: gzip, deflate' \
    -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' \
    -H 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 15_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1' \
    -H 'X-Requested-With: XMLHttpRequest' \
    -d "action=login&Password=$passenc&Username=$login&_sessionTOKEN=$ses_token" \
    --compressed \
    --insecure)

sess_token=$(echo $login_req|grep -oP '(?<="sess_token":")[^"]*')
echo "sess_token $sess_token"

#ntp=$(curl -s -b cookie.txt "${ipont}/?_type=hiddenData&_tag=sntp_data&_=$dt1" \
# -H 'Accept: */*' \
# -H 'Accept-Language: id' \
# -H 'Connection: keep-alive' \
# -H 'DNT: 1' \
# -H 'Referer: ${ipont}/' \
# -H 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 15_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1' \
# -H 'X-Requested-With: XMLHttpRequest' \
# --compressed \
# --insecure)
#echo "ntp $ntp"

##menu wan status - buka menu dulu baru kirim request status wan
wan_view=$(curl -s -b cookie.txt "${ipont}/?_type=menuView&_tag=ethWanStatus&Menu3Location=0&_="$(date +%s)"" \
    -H 'Accept: */*' \
    -H 'Accept-Language: id,en-US;q=0.9,en;q=0.8,gl;q=0.7' \
    -H 'Connection: keep-alive' \
    -H 'DNT: 1' \
    -H 'Referer: ${ipont}/' \
    -H 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 15_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1' \
    --compressed \
    --insecure)


wan_req2=$(curl -s -b cookie.txt "${ipont}/?_type=menuData&_tag=wan_internetstatus_lua.lua&TypeUplink=2&pageType=1&_="$(date +%s)"" \
    -H 'Accept: application/json, text/javascript, */*; q=0.01' \
    -H 'Accept-Language: id,en-US;q=0.9,en;q=0.8,gl;q=0.7' \
    -H 'Connection: keep-alive' \
    -H 'DNT: 1' \
    -H 'Referer: ${ipont}/' \
    -H 'Accept-Encoding: gzip, deflate' \
    -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' \
    -H 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 15_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1' \
    -H 'X-Requested-With: XMLHttpRequest' \
    --compressed \
    --insecure)

#xml block
#<ajax_response_xml_root>..
##<ID_WAN_COMFIG>
###<Instance>
####...
####<ParaName>IPAddress</ParaName>
####<ParaValue>108.137.165.4</ParaValue>
####..
###</Instance>
##</ID_WAN_COMFIG>
#</ajax_response_xml_root>

wanip=$(echo $wan_req2  |  grep -oP '(?<=<ParaName>IPAddress</ParaName><ParaValue>).+?(?=</)'|grep -v 0.0.0)

if [ "${wanip%%.*}" = "10" ]; then
    ippublic=$(curl -s ipv4.icanhazip.com)
    echo "Dapat IP Private $wanip - $ippublic"
    echo "let's start Hunt IP Pub $(date +%d%m%Y-%H%M%S)"
    curl  -s -b cookie.txt "http://192.168.1.1/?_type=menuView&_tag=ethWanConfig&Menu3Location=0&_="$(date +%s)"" \
  -H 'Accept: */*' \
  -H 'Accept-Language: id,en-US;q=0.9,en;q=0.8,gl;q=0.7' \
  -H 'Connection: keep-alive' \
  -H 'DNT: 1' \
  -H 'Referer: http://192.168.1.1/' \
  -H 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 15_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1' \
  -H 'X-Requested-With: XMLHttpRequest' \
  --compressed \
  --insecure
  
    refresh=$(curl -s -b cookie.txt 'http://192.168.1.1/?_type=menuData&_tag=wan_internet_lua.lua&TypeUplink=2&pageType=0' \
  -H 'Accept: */*' \
  -H 'Accept-Language: id,en-US;q=0.9,en;q=0.8,gl;q=0.7' \
  -H "Check: cVK7rtfEzt+Nxq1DXlu22U6E+6zC00wLU4jeJNTHd/mrmEcmzolMFzJCatTmsNArfzySBfGhDZeNKiI/FBfkbPwMvPIFZm5tLYYfGIDfntL/WKD/hYDYSMGPti6jCmVAJtOymAdOP++HSuLmuZ6RRTjT8u8NCCriC2KVY+JOvMMjTEfSHvBGKOX4xwODUQucjAArIwi738/vBY0rJI/8eUCE4BDjBFFzqCWqGm5XcrIwJ/Qs4JrWfKJowsgOW5UK5h3sZlwwRNs68m0HWlvFEsddtdRXsQ6kSLnO3zYTmjL4H9lMjMe3AjzyHfNMnv7aBK8jT6njYhx4SousUj37gg==" \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' \
  -H 'DNT: 1' \
  -H 'Origin: http://192.168.1.1' \
  -H 'Referer: http://192.168.1.1/' \
  -H 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 15_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1' \
  -H 'X-Requested-With: XMLHttpRequest' \
  --data-raw "IF_ACTION=Apply&_InstID=DEV.IP.IF5&uplink=2&InstHasGot=1&ControlType=1&WANCName=omci_ipv4_pppoe_1&Enable=1&mode=route&ServList=7&MTU=1492&linkMode=PPP&TransType=PPPoE&UserName=encrypteduser&Password=encryptedPass&AuthType=PAP%2CCHAP%2CMS-CHAP&ConnTrigger=AlwaysOn&IdleTime0=20&IdleTime1=0&IpMode=Both&Addressingtype=DHCP&IPAddress0=&IPAddress1=&IPAddress2=&IPAddress3=&SubnetMask0=&SubnetMask1=&SubnetMask2=&SubnetMask3=&GateWay0=&GateWay1=&GateWay2=&GateWay3=&DNS10=0&DNS11=0&DNS12=0&DNS13=0&DNS20=0&DNS21=0&DNS22=0&DNS23=0&DNS30=0&DNS31=0&DNS32=0&DNS33=0&IsNAT=1&IPv6AcquireMode=Auto&Gua1=&Gua1PrefixLen=128&Gateway6=&Pd=&PdLen=&Dns1v6=&Dns2v6=&Dns3v6=&IsPD=1&Unnumbered=0&IsSLAAC=0&IsGUA=0&IsPdAddr=1&VlanEnable=1&VLANID=2982&Priority=7&Btn_cancel_internet=&Btn_apply_internet=&encode=IcEniR%2Fq0T%2FsEjWDfzPLFdihF1IjXtj%2BqY%2BYeSExm%2B4w%2F9UJirIMISVQ9gGB%2BduQl3LcxCU6rmAGBod2Ff8mWMDvHGgWxJFjSKbXuRfbtaF5qopfpNm6%2F89mdSj8KkeT5htCZM%2FeK2l1Z2rPzzg1%2Bmbs1RMMrotaSFPu%2B68dNb6MXmLa55IItXOoSEHiOQ2zZQ1mLGRzHiCKPRjWV3G4bkTELiIf5lp6j5d37PTbK3h34I30Ep6bxVyuzW7ucckIVemoAFxRQZKqU4ZQo8caGImdyUPhkhDhFHC7%2FIVceWXDmZCG5I0wJJe1YckCax3ulEZdme5tbR6ZHUrlqEP8GA%3D%3D&_sessionTOKEN=$sess_token" \
  --compressed \
  --insecure)
 
  
fi
