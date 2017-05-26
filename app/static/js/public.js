function claim(id){
	var req_id = id;
	$.ajax({
		url : "/claim",
		type : "POST",
		dataType: "json",
		data : {"req_id":req_id},
		success : function(data,status){
			if (status == "success"){
				alert(data.message);
				location.reload();
				}
			else{
				alert('请求失败！');
			}}
	});
}
function upline(id){
	var req_id = id;
	$.ajax({
		url : "/upline",
		type : "POST",
		dataType: "json",
		data : {"req_id":req_id},
		success : function(data,status){
			if (status == "success"){
				alert(data.message);
				location.reload();
				}
			else{
				alert('请求失败！');
			}}
	});
}
function dateFilter(content){
	var code;
	if (content == "请选择"){
		code = 0;
	}
	else if (content == "一周内"){
		code = 1;
	}
	else if (content =="一月内" ){
		code = 2;
	}
	else{
		code = 3;
	}
	return code;
}
function queryFunc(){
	var status = $('#status option:selected').val();
	var raise_date = dateFilter($('#raise_date option:selected').val());
	var upline_date = dateFilter($('#upline_date option:selected').val());
	var raise_man = $("#raise_man").val();
	var test_man = $('#test_man').val();
	if (status == "请选择"){
		status = 0;
	}
	else if(status == "已提测"){
		status = 1;
	}
	else if(status == "测试中"){
		status = 2;
	}
	else{
		status = 3;
	}
	var path = "/getAllReq?status="+status+"&raise_date="+raise_date+"&upline_date="+upline_date+"&raise_man="+raise_man+"&test_man="+test_man+"&pageNum=1";
	window.location.href = path;
	
}
function nextFunc(){
	var pn = parseInt(GetQueryString("pageNum")) + 1;
	var pt = replaceParamVal("pageNum",pn);
	var url = this.location.href.toString();
	if (url.indexOf("?") == -1){
		pt = pt + "?pageNum=1";
	}
	else if(pt == url){
		pt = pt + "&pageNum=1"
	}
	//alert(pt);
	window.location.href = pt;
	
}
function lastFunc(){
	var pn = parseInt(GetQueryString("pageNum")) - 1;
	var pt = replaceParamVal("pageNum",pn);
	window.location.href = pt;	
}
function gotoFunc(pageNum){
	var pn = pageNum;
	var pt = replaceParamVal("pageNum",pn);
	var url = this.location.href.toString();
	if (url.indexOf("?") == -1){
		pt = pt + "?pageNum=" + pageNum;
	}
	else if(pt == url){
		pt = pt + "&pageNum=" + pageNum;
	}
	//alert(pt);
	window.location.href = pt;
}
function replaceParamVal(paramName,replaceWith) {
    var oUrl = this.location.href.toString();
    var re=eval('/('+ paramName+'=)([^&]*)/gi');
    var nUrl = oUrl.replace(re,paramName+'='+replaceWith);
    //this.location = nUrl;
    return nUrl;
}
function GetQueryString(name)
{
     var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
     var r = window.location.search.substr(1).match(reg);
     if(r!=null)return  unescape(r[2]); return null;
}

function ajaxRequest(url,method,dataType,data){
	$.ajax({
        url: url,
        method: method,
        dataType: dataType,
        data: data,
        beforeSend: function() {
        },
        success:function(data){
        	if(data.code != "1000")
        	{
        		alert(data.message);
        		}
        	else{
        		alert("操作成功");
        	}
        },
        error:function(XMLHttpRequest, textStatus, errorThrown){
        	alert(XMLHttpRequest.status);
        }
	});
}
function selectFocus(target){  
    document.getElementById(target).setAttribute("size","5");  
}  
function selectClick(target){  
    document.getElementById(target).removeAttribute("size");  
    document.getElementById(target).blur();  
    this.setAttribute("selected","");  
}  