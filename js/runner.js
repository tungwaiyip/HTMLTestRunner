output_list = Array();

/* Level - 0: Summary; 1: Failed; 2: All; 3: Skipped */
function showCase(level) {
    table_rows = document.getElementsByTagName("tr");
    for (var i = 0; i < table_rows.length; i++) {
        row = table_rows[i];
        id = row.id;
        if (id.substr(0,2) == 'ft') {
            if (level < 1) {
                row.classList.add('hiddenRow');
            }
            else {
                row.classList.remove('hiddenRow');
            }
        }
        if (id.substr(0,2) == 'pt') {
            if (level > 1) {
                row.classList.remove('hiddenRow');
            }
            else {
                row.classList.add('hiddenRow');
            }
        }
    }
}


function showClassDetail(class_id, count) {
    var testcases_list = Array(count);
    var all_hidden = true;
    for (var i = 0; i < count; i++) {
        testcase_postfix_id = 't' + class_id.substr(1) + '.' + (i+1);
        testcase_id = 'f' + testcase_postfix_id;
        testcase = document.getElementById(testcase_id);
        if (!testcase) {
            testcase_id = 'p' + testcase_postfix_id;
            testcase = document.getElementById(testcase_id);
        }
        testcases_list[i] = testcase;
        if (testcase.classList.contains('hiddenRow')) {
            all_hidden = false;
        }
    }
    for (var i = 0; i < count; i++) {
        testcase = testcases_list[i];
        if (!all_hidden) {
            testcase.classList.remove('hiddenRow');
        }
        else {
            testcase.classList.add('hiddenRow');
        }
    }
}


function showTestDetail(div_id){
    var details_div = document.getElementById(div_id)
    var displayState = details_div.style.display
    // alert(displayState)
    if (displayState != 'block' ) {
        displayState = 'block'
        details_div.style.display = 'block'
    }
    else {
        details_div.style.display = 'none'
    }
}


function html_escape(s) {
    s = s.replace(/&/g,'&amp;');
    s = s.replace(/</g,'&lt;');
    s = s.replace(/>/g,'&gt;');
    return s;
}

/* obsoleted by detail in <div>
function showOutput(id, name) {
    var w = window.open("", //url
                    name,
                    "resizable,scrollbars,status,width=800,height=450");
    d = w.document;
    d.write("<pre>");
    d.write(html_escape(output_list[id]));
    d.write("\n");
    d.write("<a href='javascript:window.close()'>close</a>\n");
    d.write("</pre>\n");
    d.close();
}
*/
