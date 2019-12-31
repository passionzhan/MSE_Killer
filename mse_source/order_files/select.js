$(function() {
	loadingBgAdd();
	if (packageListfn>0) {
		$("#projectType a:first-child").click();
		eachRegExamInfolist(regExamInfoList, nowDate);
	}
	var str = '';
	$("a[class='selected']").each(function() {
		var $id = $(this).parent().attr("id");
		var text = $(this).text();
		if ($id != "projectType") {
			str += '<div name="' + $id + '" id="' + $(this).attr("attrval") + '" class="selectedInfor selectedShow">' + '<label>' + text + '</label></div>';
		}
	});
	$("div[class='clearList']").append(str);
	eachRegExamInfolist(regExamInfoList, nowDate);
	loadingBgRemove();
});
function addPrompt() {
	$("#table").nextAll().detach();
	$("#table").after('<table width="100%"><tr><td colspan="6" height="35px" style="color: red;background-color: #efefef;text-align: center;">请正确选择：报考考点、科目和考次名称，方可继续完成报名 </td></tr></table>');
}
$(".listIndex dd a ").live("click",
function() {
	var $dd = $(this).parents("dd");
	var $id = $dd.attr("id");
	var otext = '';
	var $attrval = $(this).attr("attrval");
	if ($id == "categorylist") {
		$('.clearList div[name="projectType"]').remove();
	}
	if (eval(subIsMultiple)) {
		if ($id == "projectType") {
			$(this).addClass("selected");
			$("#" + $id + " a[class='selected']").each(function(i) {
				if (i == 0) {
					otext += $(this).html();
				} else {
					otext += "、" + $(this).html();
				}
			});
			otext = $(this).html();
		} else {
			$(this).addClass("selected").siblings().removeClass("selected");
			otext = $(this).html();
		}
		if (typeof($('.clearList div[name="' + $id + '"]')) != "undefined" && $id != "projectType") {
			$('.clearList div[name="' + $id + '"]').remove();
		}
		var tem = true;
		if ($id == "projectType") {
			$('.clearList div[name="projectType"]').each(function() {
				if ($(this).children("label").html() == otext) {
					tem = false;
				}
			});
		}
		if (tem) {
			var str = '<div name="' + $id + '" id="' + $attrval + '" class="selectedInfor selectedShow"><label>' + otext + '</label></div>';
			$("div .clearList").append(str);
		}
	} else {
		$(this).addClass("selected").siblings().removeClass("selected");
		otext = $(this).html();
		if (typeof($('.clearList div[name="' + $id + '"]')) != "undefined") {
			$('.clearList div[name="' + $id + '"]').remove();
		}
		var str = '<div name="' + $id + '" id= "' + $attrval + '" class="selectedInfor selectedShow"><label>' + otext + '</label></div>';
		$("div .clearList").append(str);
	}
	loadingBgAdd();
	$("#table").nextAll().detach();
	if($id!='categorylist'){
		getList($id);
	}else{
		getSubjectList();
	}
	loadingBgRemove();
});
$(".selectedShow em").live("click",
function() {
	var select = $(this).parent().prev().attr("name");
	var name = $(this).prev().html();
	$(this).parent().remove();
	var $id = $(this).parent().attr("name");
	$("#" + $id + " a:contains(" + name + ")").removeClass("selected");
	$("#table").nextAll().detach();
	loadingBgAdd();
	$("#table").nextAll().detach();
	getList($id);
	if ($("input[name='checkbox']").length > 0) {
		$("#submit_but").show();
	} else {
		$("#submit_but").hide();
	}
	loadingBgRemove();
});
function getSubjectList(){
    
    var categoryId = $("#categorylist a[class='selected']").attr("attrval");
    if (typeof(categoryId) == "undefined" || categoryId == '') {
       return;
    }
    $.ajax({
        url: linaUrl + "/select/getSubjectList",
        cache: false,
        async: false,
        data: {
            'proId': proId,
            'categoryId': categoryId
        },
        type: "GET",
        dataType: 'json',
        error: function(request) {
            showAlertModel("请求超时，请刷新页面。");
            loadingBgRemove();
        },
        success: function(response) {
            if (response.sessionTimeOut) {
                window.location.href = loginUrl + "/new";
                return;
            }
            if (response.msg == 'sessionTimeOut') {
                window.location.href = loginUrl + "/new?out=3";
                return;
            }
			var str = '';
			$(response.projectlist).each(function(i) {
				str += '<a href="javascript:void(0)" attrval="' + this.uniteId + '">' + this.packageName + '</a>';
			});

            $("#projectType").empty();
            $("#projectType").append(str);
			$("#orglist").empty();
            $("#table").nextAll().detach();
             $("#submit_but").hide();
        }
    });
    loadingBgRemove();

}
function getAddr() {
	loadingBgAdd();
	var geoId = $("select[name='addr'] option:selected").attr("id");
	$.ajax({
		type: "POST",
		url: linaUrl + "/select/getSenterQueryList",
		data: {
			'geoId': geoId,
			'geoId2': '',
			'proId': proId
		},
		async: false,
		dataType: 'json',
		error: function() {
			alert("出错了！");
		},
		success: function(response) {
			if (response.sessionTimeOut) {
				window.location.href = loginUrl + "/new";
				return;
			}
			if (response.msg == 'sessionTimeOut') {
				window.location.href = loginUrl + "/new?out=3";
				return;
			}
			if (response != null) {
				var str2 = '';
				$(response.addr2).each(function (i) {
					str2 += '<option id="' + this.fullId + '">' + this.name + '</option>';
				});
				$("select[name='provinces']").empty();
				$("select[name='provinces']").append(str2);
				getAddr2();
			}
		}
	});
	loadingBgRemove();
}
function getAddr2() {
	loadingBgAdd();
	var geoId = $("select[name='addr'] option:selected").attr("id");
	if (area == "1") {
		geoId = $("select[name='provinces'] option:selected").attr("id");
	}
	if (typeof(geoId) == "undefined") {
		geoId = "000000";
	}
	var studentType = $("#StudentType a[class='selected']").attr("attrval");
	if (typeof(studentType) == "undefined") {
		studentType = "08";
	}
	var timeId = $("#time_id a[class='selected']").attr("attrval");
	if (typeof(timeId) == "undefined") {
		timeId = '*';
	}
	var projectType = '';
	$("#projectType a[class='selected']").each(function() {
		projectType += $(this).attr("attrval") + ',';
	});
	if (typeof(projectType) == "undefined" || projectType == '') {
		projectType = '*';
	}
	var categoryId = $("#categorylist a[class='selected']").attr("attrval");
	if (typeof(categoryId) == "undefined" || categoryId == '') {
		categoryId = '';
	}
	$.ajax({
		type: "POST",
		url: linaUrl + "/select/getAttr?cbd=knight",
		data: {
			'geoId': geoId,
			'proId': proId,
			'category': categoryId,
			'studentType': studentType,
			'timeId': timeId,
			'subjectId': projectType
		},
		async: false,
		dataType: 'json',
		error: function() {
			showAlertModel("请求超时，请刷新页面。");
			loadingBgRemove();
		},
		success: function(response) {
			if (response.sessionTimeOut) {
				window.location.href = loginUrl + "/new";
				return;
			}
			if (response.msg == 'sessionTimeOut') {
				window.location.href = loginUrl + "/new?out=3";
				return;
			}
			if (response != null) {
				var str2 = '';
				$(response.orglist).each(function(i) {
					str2 += '<a href="javascript:void(0)" attrval="' + this.relationshipId + '">' + this.exaOrgName + '</a>';
				});
			}
			$("#orglist").empty();
			$("#orglist").append(str2);
			$("#table_tr").parent().parent().nextAll().detach();
			$("#submit_but").hide();
			$("div[class='clearList']").empty();
			init_selected();
			if (response.nowDate != null && response.nowDate != '') {
				eachRegExamInfolist(response.regExamInfolist, response.nowDate);
			}
		}
	});
	loadingBgRemove();
	return false;
}
function init_selected() {
	var str = '';
	$("a[class='selected']").each(function() {
		var $id = $(this).parent().attr("id");
		var text = $(this).text();
		str += '<div name="' + $id + '" id="' + $(this).attr("attrval") + '" class="selectedInfor selectedShow">' + '<label>' + text + '</label></div>';
	});
	$("div[class='clearList']").append(str);
}
function getList(onid) {
	var geoId = $("select[name='addr'] option:selected").attr("id");
	if (area == "1") {
		geoId = $("select[name='provinces'] option:selected").attr("id");
	}
	if (typeof(geoId) == "undefined" || geoId == '') {
		return;
	}
	var studentType = $("#StudentType a[class='selected']").attr("attrval");
	if (typeof(studentType) == "undefined" || studentType == '') {
		studentType = "08";
	}
	var timeId = $("#time_id a[class='selected']").attr("attrval");
	if (typeof(timeId) == "undefined" || timeId == '') {
		return;
	}
	var projectType = '';
	$("#projectType a[class='selected']").each(function() {
		projectType += $(this).attr("attrval") + ',';
	});
	if (typeof(projectType) == "undefined" || projectType == '') {
		projectType = '*';
	}
	var selectOrgId = $("#orglist a[class='selected']").attr("attrval");
	if (typeof(selectOrgId) == "undefined") {
		addPrompt();
		selectOrgId = '*';
	}
	var categoryId = $("#categorylist a[class='selected']").attr("attrval");
	if (typeof(categoryId) == "undefined" || categoryId == '') {
		categoryId = '';
	}
	$.ajax({
		url: linaUrl + "/select/getList?cbd=knight",
		cache: false,
		async: false,
		data: {
			'proId': proId,
			'geoId': geoId,
			'orgId': selectOrgId,
			'projectId': projectType,
			'timeId': timeId,
			'categoryId': categoryId,
			'studentType': studentType,
			'onid': onid
		},
		type: "GET",
		dataType: 'json',
		error: function(request) {
			showAlertModel("请求超时，请刷新页面。");
			loadingBgRemove();
		},
		success: function(response) {
			if (response.sessionTimeOut) {
				window.location.href = loginUrl + "/new";
				return;
			}
			if (response.msg == 'sessionTimeOut') {
				window.location.href = loginUrl + "/new?out=3";
				return;
			}
			var studentTypeVal = response.studentType;
			if ("projectType" == onid || "time_id" == onid) {
				var str = '';
				$(response.orgList).each(function(i) {
					if (this.relationshipId == selectOrgId) {
						str += '<a href="javascript:void(0)" class="selected" attrval="' + this.relationshipId + '">' + this.exaOrgName + '</a>';
					} else {
						str += '<a href="javascript:void(0)" attrval="' + this.relationshipId + '">' + this.exaOrgName + '</a>';
					}
				});
				if ("time_id" == onid) {
					str = str.replace(new RegExp('class="selected"', "gm"), '');
				}
				$("#orglist").empty();
				$("#orglist").append(str);
			}			

			
			
			if("orglist" == onid ||"time_id" == onid ||"categorylist" == onid){
				var str = '';
				var arr= new Array();
				 arr = projectType.split(","); 
				$(response.projectlist).each(function(index) {
					var tem = false;
					for (i = 0; i < arr.length; i++) {
						if (this.uniteId == arr[i]) {
							tem = true;
							break;
						}
					}
				    if(tem){
						str +='<a href="javascript:void(0)" class="selected" attrval="'+this.uniteId+'">'+this.packageName+'</a>';
					}else{
						str +='<a href="javascript:void(0)" attrval="'+this.uniteId+'">'+this.packageName+'</a>';
					}
				});
             if("time_id" == onid){
                  str = str.replace(new RegExp('class="selected"',"gm"),'');
             }
				$("#projectType").empty();
				$("#projectType").append(str);
			}
			
			
			$("#table").nextAll().detach();
			$("#submit_but").hide();
			subIsMultiple = response.subIsMultiple;
			if (!eval(subIsMultiple)) {
				$("#projectType a[class='selected']").each(function(i) {
					if (i > 0) {
						$(this).removeClass("selected");
						$("#" + $(this).attr("attrval")).detach();
					}
				});
			}
			if (typeof(selectOrgId) != "undefined" && response.nowDate != null && response.nowDate != '') {
				var noteName = response.nextNode;
				$("#submit_but button").html("下一步:" + noteName);
				eachRegExamInfolist(response.regExamInfolist, response.nowDate);
			}
		}
	});
}
function eachRegExamInfolist(regExamInfolist, nowDate) {
	var str3 = '';
	$(regExamInfolist).each(function(i) {
		var temp = true;
		var totalprice = parseFloat(this.price).toFixed(2);
		var a_msg = '';
		var packageId = '';
		$(this.regExamInfos).each(function() {
			if (temp && this.goodsType == "2") {
				if (this.status == 5 || (nowDate - this.regEndDate) > 0) {
					temp = false;
				}
				if (temp) {
					if ((nowDate - this.regStartDate) < 0) {
						temp = false;
					}
				}
				if (temp) {
					if (this.status == 9) {
						temp = false;
					}
				}
				if (temp) {
					if (this.status == 4 && (nowDate - this.regStartDate) > 0) {
						if (isBalance == "1") {
							if (parseFloat(totalprice) > parseFloat(balance)) {
								if (balanceMsg == '余额不足' || balanceMsg == '考试券额和余额不足') {
									a_msg = '<a  target="view_window" href='+advanceUrl+'?proId=' + proId + '>立即充值</a>';
								}
								temp = false;
							}
						}
						if (a_msg == '' && !this.capacity) {
							temp = false;
						}
					} else {
						temp = false;
					}
				}
			}
			packageId = this.packageId;
		});
		var chackox = "";
		if (temp) {
			if (eval(subIsMultiple)) {
				chackox = '<input name="checkbox" type="checkbox" >';
			} else {
				chackox = '<input name="checkbox" type="radio" >';
			}
		}
		str3 += '<table class="store_cart_content"><tr class="cart_goods" style="line-height: 30px;">' + '<td class="cart_goods"  style="text-align: center;">' + chackox + '<input type="hidden" name="selectId" value="' + this.categoryId + '"><input type="hidden" name="packageId" value="' + packageId + '"></td><td colspan="3" style="text-align: left;">' + this.categoryName + '</td><td>' + a_msg + '</td><td>' + totalprice + '</td></tr>';
		var pag = '<input type="hidden" name="categoryId" value="' + this.categoryId + '">';
		$(this.regExamInfos).each(function() {
			var stat = '';
			if (this.goodsType == "2") {
				if (this.status == "5" || (nowDate - this.regEndDate) > 0) {
					stat = '报名已结束';
				}
				if (stat == '') {
					if ((nowDate - this.regStartDate) < 0) {
						stat = '报名未开始';
					}
				}
				if (stat == '') {
					if (this.status == "9") {
						stat = '暂停报名';
					}
				}
				if (stat == '') {
					if (this.status == "4" && (nowDate - this.regStartDate) > 0) {
						if (isBalance == "1") {
							if (parseFloat(totalprice) > parseFloat(balance)) {
								stat = balanceMsg;
							} else {
								if (this.capacity) {
									stat = '可报考';
								} else {
									stat = '名额暂满';
								}
							}
						} else {
							if (this.capacity) {
								stat = '可报考';
							} else {
								stat = '名额暂满';
							}
						}
					} else {
						stat = '报名未开始';
					}
				}
			}
			str3 += '<tr class="tr_goods"><td width="10%">' + pag + '<input type="hidden" name="packageId" value="' + this.packageId + '">' + '<input type="hidden" name="orgGeo" value="' + this.orgGeo + '">' + '<input type="hidden" name="relationshipId" value="' + this.relationshipId + '">' + '<input type="hidden" name="examId" value="' + this.examId + '">' + '<input type="hidden" name="examDate" value="' + this.examDate + '">' + '<input type="hidden" name="subjectId" value="' + this.subjectId + '"></td>' + '<td width="22%">' + this.subjectName + '</td>';
			if (this.goodsType == "2") {
				str3 += '<td width="24%">' + this.orgName + '</td>' + '<td width="17%">' + this.examDate + '</td>';
			} else {
				str3 += '<td width="24%"></td><td width="17%"></td>';
			}
			str3 += '<td width="15%">' + stat + '</td><td width="12%">' + '' + '</td></tr>';
		});
		str3 += '</table>';
	});
	$("#table").nextAll().detach();
	if (str3 == '') {
		str3 = '<table width="100%"><tr><td colspan="6" height="35px" style="text-align: center;">没有可报考的科目。 </td></tr></table>';
	}
	$("#table").after(str3);
	if ($("input[name='checkbox']").length > 0) {
		$("#submit_but").show();
	} else {
		$("#submit_but").hide();
	}
}
function valiExameDate() {
	var isFlag = true;
	$("input:checked[name='checkbox']").each(function(i) {
		if (isFlag) {
			var packageId = $(this).nextAll("input[name='packageId']").val();
			$(this).parent().parent().nextAll().each(function() {
				var goods_tr = $(this);
				var examDate = goods_tr.children().eq(0).children("[name='examDate']").val();
				var nsubjectId = goods_tr.children().eq(0).children("[name='subjectId']").val();
				$("input:checked[name='checkbox']").each(function() {
					if (isFlag) {
						var npackageId = $(this).nextAll("input[name='packageId']").val();
						$(this).parent().parent().nextAll().each(function() {
							var nexamDate = $(this).children().eq(0).children("[name='examDate']").val();
							if (packageId != npackageId && nexamDate == examDate) {
								isFlag = false;
								showAlertModel("请检查是否勾选了相同考试时间的科目，或到'个人中心-我的报考'下查看是否存在报考订单！");
								loadingBgRemove();
							}
							var subjectId = $(this).children().eq(0).children("[name='subjectId']").val();
							if (packageId != npackageId && subjectId.substr(0, 4) != nsubjectId.substr(0, 4)) {
								isFlag = false;
								showAlertModel("只能报考同一级别。请检查是否勾选了不同类别的科目，或到'个人中心-我的报考'下查看是否存在报考订单！");
								loadingBgRemove();
							}
						});
					}
				});
			});
		}
	});
	return isFlag;
}
function submit() {
	loadingBgAdd();
	var tr = '';
	var packageId = '';
	if ($("input[name='checkbox']:checked").length > 0) {
		if ("1" == examTimeConflict) {
			if (!valiExameDate()) {
				loadingBgRemove();
				return false;
			}
		}
		if (svorelistSize > 0 && $("input:checked[type='radio'][name='score']").length == 0) {
			showAlertModel("请选择使用前次合格成绩或者放弃。");
			loadingBgRemove();
			return false;
		}
		var temp = true;
		var scoreVal = '';
		$("input:checked[name='checkbox']").each(function(i) {
			$(this).parent().parent().nextAll().each(function() {
				var subid = $(this).children().eq(0).children("[name='subjectId']").val();

				scoreVal = $("input[type='radio'][name='score']:checked").val();

				if (typeof(scoreVal) != "undefined" && scoreVal.length > 4) {

					if (subid.substring(0, 4) != scoreVal.substring(0, 4)) {
						temp = false;
					}

					if (temp && $("input:checked[type='radio'][name='score'][value='" + subid + "']").length != 0) {
						temp = false;
					}
				} else {
					scoreVal = '';
				}
			});
		});
		if (!temp) {
			showAlertModel("所选成绩不能用。");
			loadingBgRemove();
			return;
		}
		$("input:checked").each(function(i) {
			tr += '<tr>';
			$(this).parent().parent().nextAll().each(function() {
				$(this).children().eq(0).children().each(function() {
					var name = $(this).attr("name");
					tr += '<input type="hidden" name="regList[' + i + '].' + name + '" value="' + $(this).val() + '">';
				});
			});
			packageId += $(this).nextAll("input[name='selectId']").attr("value") + "#";
		});
		var studentType = $("#StudentType a[class='selected']").attr("attrval");
		if (typeof(studentType) == "undefined") {
			studentType = "08";
		}
		var timeId = $("#time_id a[class='selected']").attr("attrval");
		if (typeof(timeId) == "undefined") {
			timeId = "*";
		}
		var selectOrgId = $("#orglist a[class='selected']").attr("attrval");
		if (typeof(selectOrgId) == "undefined") {
			selectOrgId = "*";
		}
		var geoId = $("select[name='addr'] option:selected").attr("id");
		if (area == "1") {
			geoId = $("select[name='provinces'] option:selected").attr("id");
		}
		if (typeof(geoId) == "undefined") {
			geoId = "000000";
		}
		tr += '<input type="hidden" name="uId" value="'+uId+'"><input ' + 'type="hidden" name="proId" value="' + proId + '"><input type="hidden" name="nodeCode" ' + 'value="'+nodeCode+'"><input type="hidden" name="studentType"' + 'value="' + studentTypeVal + '"><input type="hidden" name="examId" value="' + timeId + '">' + '<input type="hidden" name="orgGeo" value="' + geoId + '">' + '<input type="hidden" name="paymentType" value="'+paymentType+'">' + '<input type="hidden" name="scoreId" value="' + scoreVal + '">' + '<input type="hidden" name="packageId" value="' + packageId + '">' + '<input type="hidden" name="relationshipId" value="' + selectOrgId + '"></tr>';
		$("form").append(tr);
		$.ajax({
			url: linaUrl + "/"+proId+"Index/confirmation",
			async: false,
			data: $("form").serialize(),
			type: "POST",
			dataType: 'json',
			error: function(request) {
				showAlertModel("请求超时，请刷新页面。");
				loadingBgRemove();
			},
			success: function(data) {
				if (data.sessionTimeOut) {
					window.location.href = loginUrl + "/new";
					return;
				}
				if (data.msg == 'sessionTimeOut') {
					window.location.href = loginUrl + "/new?out=3";
					return;
				}
				if (data.success) {
					window.location.href = data.nextUrl;
				} else {
					showAlertModel(data.msg);
					loadingBgRemove();
				}
			}
		});
		$("form").empty();
	} else {
		showAlertModel("请选择报考");
		loadingBgRemove();
	}
}

function getAddr2() {
	loadingBgAdd();
	var geoId = $("select[name='addr'] option:selected").attr("id");
	if (area == "1") {
		geoId = $("select[name='provinces'] option:selected").attr("id");
	}
	if (typeof(geoId) == "undefined") {
		geoId = "000000";
	}
	var studentType = $("#StudentType a[class='selected']").attr("attrval");
	if (typeof(studentType) == "undefined") {
		studentType = "08";
	}
	var timeId = $("#time_id a[class='selected']").attr("attrval");
	if (typeof(timeId) == "undefined") {
		timeId = '*';
	}
	var projectType = '';
	$("#projectType a[class='selected']").each(function() {
		projectType += $(this).attr("attrval") + ',';
	});
	if (typeof(projectType) == "undefined" || projectType == '') {
		projectType = '*';
	}
	var categoryId = $("#categorylist a[class='selected']").attr("attrval");
	if (typeof(categoryId) == "undefined" || categoryId == '') {
		categoryId = '';
	}
	$.ajax({
		type: "POST",
		url: linaUrl + "/select/getAttr?cbd=knight",
		data: {
			'geoId': geoId,
			'proId': proId,
			'category': categoryId,
			'studentType': studentType,
			'timeId': timeId,
			'subjectId': projectType
		},
		async: false,
		dataType: 'json',
		error: function() {
			showAlertModel("请求超时，请刷新页面。");
			loadingBgRemove();
		},
		success: function(response) {
			if (response.sessionTimeOut) {
				window.location.href = loginUrl + "/new";
				return;
			}
			if (response.msg == 'sessionTimeOut') {
				window.location.href = loginUrl + "/new?out=3";
				return;
			}
			if (response != null) {
				var str2 = '';
				$(response.orglist).each(function(i) {
					str2 += '<a href="javascript:void(0)" attrval="' + this.relationshipId + '">' + this.exaOrgName + '</a>';
				});
			}
			$("#orglist").empty();
			$("#orglist").append(str2);
			
			var str = '';
			var arr= new Array();
			 arr = projectType.split(","); 
				 $(response.packageList).each(function(index) {
						var tem = false;
						if(projectType.indexOf(this.uniteId) >= 0 ){ tem = true; }
						if(tem){
							str +='<a href="javascript:void(0)" class="selected" attrval="'+this.uniteId+'">'+this.packageName+'</a>';
						}else{
							str +='<a href="javascript:void(0)" attrval="'+this.uniteId+'">'+this.packageName+'</a>';
						}
					});
			$("#projectType").empty();
			$("#projectType").append(str);
			
			$("#table_tr").parent().parent().nextAll().detach();
			$("#submit_but").hide();
			$("div[class='clearList']").empty();
			init_selected();
			if (response.nowDate != null && response.nowDate != '') {
				eachRegExamInfolist(response.regExamInfolist, response.nowDate);
			}
		}
	});
	loadingBgRemove();
	return false;
}
function toUserPage() {
	window.location.href = linaUsercenterUserinfoUrl;
}
function toLoginPage() {
	window.location.href = logoutUrl;
}