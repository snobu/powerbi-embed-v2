// Let's get an Azure AD Bearer token and
// exchange it for Power BI embed token.

// Python backend
function get_token_embed(backendUrl) {
//var backendUrl =  "{{ backend_url }}";

// OR Azure Function C# backend
// var backendUrl = "https://FuncAppName.azurewebsites.net/api/FuncName?code=Function-Level-Authorization-Token";

$.ajax({
    url: backendUrl,
    success: result => {
        embed(result);
    },
    beforeSend: () => {
        $('#reportDiv').html('<center>' +
            '<p>Loading dashboard...</p>' +
            '<img src="img/squirrel_loading.gif" />' +
            '</center>');
    },
    complete: () => {
        // We have the ajax response
    }
});


}

function embed(result) {

    var report, reportDiv, accessToken, embedUrl, embedReportId;
    // Set filter defaults
    var outsourced = false;

    // Embed Token
    accessToken = result.embedToken

    // Read embed URL from Model
    embedUrl = result.embed_url;

    // Read report Id from Model
    embedReportId = result.report_id;

    // Get models. models contains enums that can be used.
    var models = window['powerbi-client'].models;

    // Embed configuration used to describe the what and how to embed.
    // This object is used when calling powerbi.embed.
    // This also includes settings and options such as filters.
    // You can find more information at https://github.com/Microsoft/PowerBI-JavaScript/wiki/Embed-Configuration-Details.
    var config = {
        type: 'report',
        tokenType: models.TokenType.Embed,
        accessToken: accessToken,
        embedUrl: embedUrl,
        id: embedReportId,
        permissions: models.Permissions.All,
        settings: {
                filterPaneEnabled: false,
                navContentPaneEnabled: false
        }
    };

    $(document).ready(() => {
        if (backendUrl.includes('funcapps')) {
            $('#appName').text('Power BI Embedded Demo - C# Azure Function backend');
        }
        else {
            $('#appName').text('Power BI Embedded Demo - Python backend');
        }
    });

    // Get a reference to the embedded report HTML element
    reportDiv = $('#reportDiv')[0];

    // Embed the report and display it within the div container
    report = powerbi.embed(reportDiv, config);

    // Wait for report to be loaded
    // https://github.com/Microsoft/PowerBI-JavaScript/wiki/Handling-Events
    report.on('loaded', event => {
        // Set event handlers
        $('#Mexico').click(() => {
            report.setFilters([makeLocationFilter('Mexico')])
                .then(result => {
                    console.log('Location filter set to Mexico');
                })
                .catch(errors => {
                    console.error(errors);
                });
        });

        // Be verbose about Power BI events
        report.off('dataSelected');
        report.off('filtersApplied');
        report.on('dataSelected', event => {
            var data = event.detail;
            console.log('[Power BI dataSelected event]');
            console.log(data);
        });
        report.on('filtersApplied', event => {
            var data = event.detail;
            console.log('[Power BI filtersApplied event]');
            console.log(data);
        });

        // UI Event handlers
        $('#USA').click(() => {
            report.setFilters([makeLocationFilter('USA')])
                .then(result => {
                    console.log('Location filter set to USA');
                })
                .catch(errors => {
                    console.error(errors);
                });
        });

        $('#Outsourced').click(() => {
            if ($('#Outsourced').is(':checked')) {
                report.setFilters([makeSubCatFilter('Outsourced')])
                    .then(result => {
                        console.log('Showing only Outsources subcategory.');
                        outsourced = true;
                    })
                    .catch(errors => {
                        console.error(errors);
                    });
                }
            else if (outsourced) {
                report.removeFilters([makeSubCatFilter('Outsourced')])
                .then(result => {
                    console.log('Outsourced subcategory filter removed.');
                    outsourced = false;
                })
                .catch(errors => {
                    console.error(errors);
                });
            }
        });

        $('#filterPane').click(function() {
            if ($(this).is(':checked')) {
                report.updateSettings({ 'filterPaneEnabled': true })
                    .then(result => {
                        console.log('Filter pane enabled.');
                    })
                    .catch(errors => {
                        console.error(errors);
                    });
                }
            else {
                report.updateSettings({ 'filterPaneEnabled': false })
                    .then(result => {
                        console.log('Filter pane disabled.');
                    })
                    .catch(errors => {
                        console.error(errors);
                    });
            }
        });

        $('#reportNav').click(function() {
            if ($(this).is(':checked')) {
                report.updateSettings({ 'navContentPaneEnabled': true })
                    .then(result => {
                        console.log('Navigation pane enabled.');
                    })
                    .catch(errors => {
                        console.error(errors);
                    });
                }
            else {
                report.updateSettings({ 'navContentPaneEnabled': false })
                    .then(result => {
                        console.log('Navigation pane disabled.');
                    })
                    .catch(errors => {
                        console.error(errors);
                    });
            }
        });

        $('#Print').click(function() {
            report.print()
            .then(function (result) {
                console.log('Report is printing.');
            })
            .catch(function (errors) {
                console.error(errors);
            });
        });

        // Page Navigation buttons
        report.getPages()
            .then(pages => {
                pages.forEach(page => {
                    var pageNames = 'PageName: ' + page.name + ", DisplayName: " + page.displayName;
                    var btnId = `pageBtn_${page.name}`;
                    var btn = `<button class="btn btn-warning btn-block" style="font-size: 10px" id="${btnId}">${page.displayName}</button>`
                    $('#pageButtons').append(btn);
                    $('#pageButtons').show(150); // fade in
                    var sel = $('#' + btnId);
                    sel.click(() => {
                        report.setPage(page.name)
                            .then(result => {
                                console.log(`Page set to ${page.name}`);
                            })
                            .catch(errors => {
                                console.error(errors);
                            });
                    });
                });
            })
            .catch(error => {
                console.error(error);
            });

    }); // on 'loaded'

} // embed func

// Custom nav and filters
function makeLocationFilter(location) {
    return filter = {
        $schema: "http://powerbi.com/product/schema#basic",
        target: {
            table: "Location",
            column: "Country/Region"
        },
        operator: "Contains",
        values: [location]
    };
}

// Custom nav and filters
function makeSubCatFilter(subcat) {
    return filter = {
        $schema: "http://powerbi.com/product/schema#basic",
        target: {
            table: "Item",
            column: "Sub Category"
        },
        operator: "Contains",
        values: [subcat]
    };
}