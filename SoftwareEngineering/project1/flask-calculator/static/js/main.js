$(document).ready(function() {
    var theme = ["lightblue","gray","gold"];
    var history = [];
    var sup_tag = false;
    var mainOutput = $('#output');
    var subOutput = $('#output2');

    var clearOutput = function() {
        mainOutput.html('');
        subOutput.html('');
    };

    var digitError = function() {
        mainOutput.html('0');
        subOutput.html('Reach Digit Limit');
    };

    var checkInput = function () {
        if (mainOutput.html().replace('<sup>','').replace('</sup>','').length > 18) {
            digitError();
        }
    };

    $(this).keydown( function(e) {
        checkInput();
        var key = window.event?e.keyCode:e.which;
        if(key.toString() == "13"){
            submit();
            return false;
        }
    });

    $('.show-hist').click(function() {
         $('.show-hist').popover({
				html : true
			});
    });

    $('.set-theme').click(function() {
        index = (Number($('.box').attr("id")) + 1) % 3;
        $('.box').css("background-color",theme[index])
        $('.box').attr("id",index.toString())
    });

    var submit = function() {
        if (mainOutput.html() === '' || ('+-*/').indexOf(mainOutput.html()) != -1) return ;
        $.getJSON($SCRIPT_ROOT + '/_calculate', {
            exp: $('.main-screen').text()
        }, function(data) {
            if (data.result.toString().length > 32) {
                digitError();
            } else {
                if (data.result=='#'){
                    mainOutput.html('0');
                    subOutput.html('Input Error!');
                    return;
                }
                var exp = '<li>'+mainOutput.html()+'='+data.result+'</li>';
                var content = '';
                mainOutput.html(data.result);
                subOutput.html('result as below');
                if (history.length == 0) {
                    history.push(exp);
                }
                else if (history.length < 5) {
                    history.unshift(exp);
                }
                else {
                    history.pop();
                    history.unshift(exp);
                }
                for (var i = 0;i < history.length;i++){
                    content += history[i];
                }

                $('.show-hist').attr('data-content',content);
            }
        });
    };

    $('.nums').click(function() {

        if (sup_tag == true){
            mainOutput.html(mainOutput.html().replace('?',$(this).val()));
            sup_tag = false;
            return;
        }

        // if ($(this).val() == '.' && (mainOutput.html()).indexOf('.') != -1) return ;
        if (mainOutput.html() == '0' || subOutput.html() == 'Reach Digit Limit') {
            clearOutput();
        }

        mainOutput.append($(this).val());
        // subOutput.append($(this).val());
        checkInput();
    });

    $('#clearButton').click(function() {
        mainOutput.html('0');
        subOutput.html('');
        // clearData();
    });

    $('.btn-func').click(function() {
        if (mainOutput.html() == '0' || subOutput.html() == 'Reach Digit Limit') {
            clearOutput();
            if ($(this).val().indexOf('1') != -1 || $(this).val().indexOf('2') != -1){
                subOutput.html('Input Error!');
                mainOutput.html('0');
                return;
            }
        }
        mainOutput.append($(this).val());
        checkInput();
    });

    $('.btn-func-sup').click(function() {
        if (mainOutput.html() == '0' || subOutput.html() == 'Reach Digit Limit') {
            clearOutput();
            if ($(this).val().indexOf('e')){
                subOutput.html('Input Error!');
                mainOutput.html('0');
                return;
            }
        }
        mainOutput.append($(this).val());
        sup_tag = true;
        checkInput();
    });

    $('.btn-operate').click(function() {
        if (mainOutput.html() == '0' || subOutput.html() == 'Reach Digit Limit') {
            clearOutput();
            subOutput.html('Input Error!');
            mainOutput.html('0');
            return;
        }
        mainOutput.append($(this).val());
        checkInput();
    });

    $('#resultButton').click(function() {
        submit();
    })
});