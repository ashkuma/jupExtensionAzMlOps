define(["base/js/namespace", "base/js/events"], function(Jupyter, events) {
    // ...........Parameters configuration......................
    // define default values for config parameters if they were not present in general settings (notebook.json)
    var cfg = {
        deployLocally: false,
        gitHubPatToken: "",
        AzureContainerName: "",
        AzureAKSName: ""
    };

    var configFromSetup = undefined;

    function getACRDetails() {
        if (configFromSetup != undefined && configFromSetup["ACRAccount"].length > 0) {
            return configFromSetup["ACRAccount"][0];
        }
        return undefined;
    }

    function getAKSDetails() {
        if (configFromSetup != undefined && configFromSetup["AKSCluster"].length > 0) {
            return configFromSetup["AKSCluster"][0];
        }
        return undefined;
    }

    // to be called once config is loaded, this updates default config vals
    // with the ones specified by the server's config file
    var update_params = function() {
        console.log("updaitng configs");

        var config = Jupyter.notebook.config;
        console.log(Jupyter.notebook.metadata);
        console.log(config);
        for (var key in cfg) {
            if (config.data.hasOwnProperty(key)) {
                cfg[key] = config.data[key];
            }
        }

        console.log(cfg);
    };

    function setCookie(cname, cvalue, exdays) {
        var d = new Date();
        d.setTime(d.getTime() + exdays * 24 * 60 * 60 * 1000);
        var expires = "expires=" + d.toUTCString();
        document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
    }

    function getCookie(cname) {
        var name = cname + "=";
        var ca = document.cookie.split(";");
        for (var i = 0; i < ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0) == " ") {
                c = c.substring(1);
            }
            if (c.indexOf(name) == 0) {
                return c.substring(name.length, c.length);
            }
        }
        return "";
    }

    function checkCookie() {
        var user = getCookie("username");
        if (user != "") {
            alert("Welcome again " + user);
        } else {
            user = prompt("Please enter your name:", "");
            if (user != "" && user != null) {
                setCookie("username", user, 365);
            }
        }
    }

    // this function to generate all depndencies
    function dependency_gen_callback(msg) {
        alert("dependency generated");
    }

    function deployment_complete_callback(msg) {
        var jsonVars = msg.content["text"];
        console.log(jsonVars);
    }

    function code_exec_callback(msg) {
        var jsonVars = msg.content["text"];

        try {
            configFromSetup = JSON.parse(jsonVars);
            console.log(configFromSetup);
            Jupyter.toolbar.add_buttons_group([
                Jupyter.keyboard_manager.actions.register(
                    {
                        help: "Deploy Model to Azure",
                        icon: "fa-play-circle",
                        handler: deploy_Container
                    },
                    "deploy-to-azure",
                    "Deploy Model"
                ),
                Jupyter.keyboard_manager.actions.register(
                    {
                        help: "Generate AZCredentials",
                        icon: "fa-wrench",
                        handler: generateDependencies
                    },
                    "create_dependency",
                    "Generate Dependency Files"
                )
            ]);
        } catch {
            console.log("cloud not parse");
        }
    }

    generateDependencies = function() {
        var libName = Jupyter.notebook.base_url + "nbextensions/defaultCell/" + "generateDependencies.py";
        $.get(libName)
            .done(function(data) {
                code_init = data;
                Jupyter.notebook.kernel.execute(code_init, { iopub: { output: dependency_gen_callback } }, { silent: false });
            })
            .fail(function() {
                console.log(log_prefix + "failed to load " + lib + " library");
            });
    };

    getPatTokenFromUser = function() {
        var patToken = prompt("Please enter your PAT Token", "XXXX");
        if (patToken != null) {
            return patToken;
        }
        return undefined;
    };

    var deploy_Container = function() {
        // create a docker container and then inform then system about the updates
        patToken = undefined;
        if (cfg.gitHubPatToken == undefined || cfg.gitHubPatToken == "" || cfg.gitHubPatToken == "None" || cfg.gitHubPatToken == null) {
            // take the user PAT token, save it and then add it as well.
            patToken = getPatTokenFromUser();
            if (patToken == null || patToken == undefined) {
                console.log(" Cant continue without a PAT token");
                return;
            }
        } else {
            patToken = cfg.gitHubPatToken;
        }

        console.log(" Time to deploy the container");
        var libName = Jupyter.notebook.base_url + "nbextensions/defaultCell/" + "deploytoAzure.py";
        $.get(libName)
            .done(function(data) {
                code_init = data;
                acrReplacement = getACRDetails();
                if (acrReplacement != undefined) {
                    code_init = code_init.replace("ACRPLACEHOLDER", "aaaaaademo");
                }

                aksReplacement = getAKSDetails();
                if (aksReplacement != undefined) {
                    code_init = code_init.replace("AKSNAMEPLACEHOLDER", "aaaaaaa");
                    code_init = code_init.replace("AKSRESOURCEGROUPPLACEHOLDER", "shpraka");
                }

                if (patToken != undefined) {
                    code_init = code_init.replace("GITHUBPATTOKEN", patToken);
                }

                console.log(code_init);
                Jupyter.notebook.kernel.execute(code_init, { iopub: { output: deployment_complete_callback } }, { silent: false });
            })
            .fail(function() {
                console.log(log_prefix + "failed to load " + lib + " library");
            });
    };

    // Adds a cell above current cell (will be top if no cells)
    var runSetup = function() {
        // first check if cookie is present and not expired. if that is the case then no issue else run the setup for getting subscription
        // if all values required are already here then don't call the setup.

        var libName = Jupyter.notebook.base_url + "nbextensions/defaultCell/" + "setup.py";
        $.get(libName)
            .done(function(data) {
                code_init = data;
                Jupyter.notebook.kernel.execute(code_init, { iopub: { output: code_exec_callback } }, { silent: false });
            })
            .fail(function() {
                console.log(log_prefix + "failed to load " + lib + " library");
            });
    };

    // Button to add default cell
    var initialSetup = function() {
        update_params();
        // do initial set up ready the directory structure and finding the related files
        runSetup();
    };

    var initialize = function() {
        initialSetup();
    };

    // Run on start
    function load_ipython_extension() {
        return Jupyter.notebook.config.loaded.then(initialize);
    }
    return {
        load_ipython_extension: load_ipython_extension
    };
});
