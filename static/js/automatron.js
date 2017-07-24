/*

Automatron: UI javascript

  - Pull Target info from API and update `div`
  - Pull Runbook status from API and update `div`
  - Pull Events from API and update `div`

*/


// Update Target list
function updateTargets(target) {
    "use strict";
    var status = "default";
    var hostname = target.hostname.split(".");
    var counts = {
        "OK": 0,
        "WARNING": 0,
        "CRITICAL": 0,
        "UNKNOWN": 0
    };

    $.each(target.runbooks, function (key, value) {
        // Check status and set bootstrap class accordingly
        if (value.hasOwnProperty('status')) {
            if (value.status.OK > 0 && status === "default") {
                status = "success";
            }
            if (value.status.WARNING > 0) {
                status = "warning";
            }
            if (value.status.CRITICAL > 0) {
                status = "danger";
            }
            $.each(value.status, function (k, v) {
                if (v > 0) {
                    counts[k] = counts[k] + 1;
                }
            });
        }
    });

    $("div.servers-group").append("<div class=\"col-md-4\"><div class=\"panel panel-default\"><div class=\"panel-body\"> \
    <h2><a href=\"#\" class=\"server-info\" data-target=\".server-modal-lg\" data-toggle=\"modal\" data-hostname=\"" + target.hostname + "\">" + hostname[0] + "</a> <i class=\"fa fa-server text-" + status + " pull-right\" aria-hidden=\"true\"></i></h2><hr> \
    <p class=\"text-muted lead\">" + target.hostname + " <span class=\"label label-primary\">" + target.facts.os + "</span></p><hr> \
    <span class=\"label label-success\">" + counts.OK + " OK</span> \
    <span class=\"label label-warning\">" + counts.WARNING + " WARNING</span> \
    <span class=\"label label-danger\">" + counts.CRITICAL + " CRITICAL</span> \
    <span class=\"label label-info\">" + counts.UNKNOWN + " UNKNOWN</span> \
    </div></div></div>").fadeIn("slow");
}

// Update Target Counter
function updateTargetCount(count) {
    "use strict";
    $("div.target-count").text(count).fadeIn("slow");
}

// Update Runbook OK Counter
function updateOkCount(count) {
    "use strict";
    $("div.ok-count").text(count).fadeIn("slow");
}

// Update Runbook Unknown Counter
function updateUnknownCount(count) {
    "use strict";
    $("div.unknown-count").text(count).fadeIn("slow");
}

// Update Runbook Warning Counter
function updateWarningCount(count) {
    "use strict";
    $("div.warning-count").text(count).fadeIn("slow");
}

// Update Runbook Critical Counter
function updateCriticalCount(count) {
    "use strict";
    $("div.critical-count").text(count).fadeIn("slow");
}

// Add Runbook Event to event stream
function addEvent(value) {
    "use strict";
    var hostname = value.target.split(".");
    if (value.status === "CRITICAL") {
        $("ul.status-group").append("<li class=\"list-group-item list-group-item-danger status-item\"><span class=\"badge\">" + value.status + "</span><b>" + hostname[0] + "</b>: " + value.runbook + "</li>").fadeIn("slow");
    }
    if (value.status === "OK" && value.count <= 1) {
        $("ul.status-group").append("<li class=\"list-group-item list-group-item-success status-item\"><span class=\"badge\">" + value.status + "</span><b>" + hostname[0] + "</b>: " + value.runbook + "</li>").fadeIn("slow");
    }
    if (value.status === "WARNING") {
        $("ul.status-group").append("<li class=\"list-group-item list-group-item-warning status-item\"><span class=\"badge\">" + value.status + "</span><b>" + hostname[0] + "</b>: " + value.runbook + "</li>").fadeIn("slow");
    }
    if (value.status === "UNKNOWN") {
        $("ul.status-group").append("<li class=\"list-group-item list-group-item-info status-item\"><span class=\"badge\">" + value.status + "</span><b>" + hostname[0] + "</b>: " + value.runbook + "</li>").fadeIn("slow");
    }
}

// Perform API call and process results for Status and Events
function getStatus() {
    "use strict";
    $.ajax({
        url: "/api/status",
        dataType: "json",
        success: function (json) {
            updateTargetCount(json.targets);
            updateOkCount(json.runbooks.OK);
            updateWarningCount(json.runbooks.WARNING);
            updateCriticalCount(json.runbooks.CRITICAL);
            updateUnknownCount(json.runbooks.UNKNOWN);
            // Clear existing status
            if (json.events.length >= 1) {
                $("ul.status-group").empty();
                $.each(json.events, function (key, value) {
                    addEvent(value);
                });
                if ($("li.status-item").length === 0) {
                    $("ul.status-group").append("<li class=\"list-group-item list-group-item-default status-item\">No events found</li>");
                }
            } else {
                $("ul.status-group").empty();
                $("ul.status-group").append("<li class=\"list-group-item list-group-item-default status-item\">No events found</li>");
            }
        }
    });
}

// Perform API call and process results for Target list
function getTargets() {
    "use strict";
    $.ajax({
        url: "/api/targets",
        dataType: "json",
        success: function (json) {
            $("div.servers-group").empty();
            var added = 0;
            $("div.servers-group").append("<div class=\"row\">");
            $.each(json, function (key, value) {
                if (added % 3 === 0) {
                    $("div.servers-group").append("</div><div class=\"row\">");
                }
                updateTargets(value);
                added = added + 1;
            });
            $("div.servers-group").append("</div>");
        }
    });
}


$(document).on("click", ".server-info", function() {
    "use strict";
    var name = $(this).data().hostname;
    $("h4.modal-title").text(name);
    $.ajax({
        url: "/api/targets/" + name,
        dataType: "json",
        success: function (json) {
            // Update Server info
            $("div.server-panel-info").html("<div class=\"row\">" +
            "<div class=\"col-md-6\"><b>Name:</b> " + json.hostname + "</div><div class=\"col-md-6\"><b>Operating System:</b> " + json.facts.os + "</div>" +
            "<div class=\"col-md-6\"><b>Address:</b> " + json.ip + " </div><div class=\"col-md-6\"><b>Kernel:</b> " + json.facts.kernel + "</div>" +
            "</div>")

            // Update Runbook status
            $("ul.server-runbooks-group").empty();
            $.each(json.runbooks, function (key, value) {
                if (value.last_status === "CRITICAL") {
                    $("ul.server-runbooks-group").append("<li class=\"list-group-item list-group-item-danger status-item\"><span class=\"badge\">" + value.last_status + "</span><b>" + value.name + "</b></li>");
                }
                if (value.last_status === "OK") {
                    $("ul.server-runbooks-group").append("<li class=\"list-group-item list-group-item-success status-item\"><span class=\"badge\">" + value.last_status + "</span><b>" + value.name + "</b></li>");
                }
                if (value.last_status === "WARNING") {
                    $("ul.server-runbooks-group").append("<li class=\"list-group-item list-group-item-warning status-item\"><span class=\"badge\">" + value.last_status + "</span><b>" + value.name + "</b></li>");
                }
                if (value.last_status === "UNKNOWN") {
                    $("ul.server-runbooks-group").append("<li class=\"list-group-item list-group-item-info status-item\"><span class=\"badge\">" + value.last_status + "</span><b>" + value.name + "</b></li>");
                }
            });
            if (json.runbooks.length < 0) {
                $("ul.server-runbooks-group").append("<li class=\"list-group-item list-group-item-default status-item\">No Runbooks found</li>")
            }
        }
    });
});


// Wrapper run function
function run() {
    "use strict";
    getStatus();
    getTargets();
}


// Run run() on load and every 10 seconds
window.onload = run();
window.setInterval(function () {
    "use strict";
    run();
}, 10000);
