// XBlock runtime implementation.
define(["jquery", "jquery.immediateDescendents"], function($) {
    // Constructors for a runtime object provided to an XBlock init function.
    // Indexed by version number.  Only 1 right now.
    var runtime_constructors = {
        1: function (element, children) {
            var child_map = {};
            $.each(children, function(idx, child) {
                child_map[child.name] = child;
            });
            return {
                handler_url: function(handler_name) {
                    var usage = $(element).data('usage');
                    return "/handler/" + usage + "/" + handler_name + "/?student=" + student_id;
                },
                children: children,
                child_map: child_map
            };
        }
    };

    var initializeBlock = function (element, init_fns) {
        var children = initializeBlocks($(element), init_fns);

        var version = $(element).data('runtime-version');
        if (version === undefined) {
            return null;
        }

        var runtime = runtime_constructors[version](element, children);
        var package_name = $(element).data('block-type');
        var init_fn = init_fns[package_name];
        var js_block = init_fn(runtime, element) || {};
        js_block.element = element;
        js_block.name = $(element).data('name');
        return js_block;
    };

    var initializeBlocks = function (element, init_fns) {
        return $(element).immediateDescendents('.xblock').map(function(idx, elem) {
            init_fns = init_fns || {};
            return initializeBlock(elem, init_fns);
        }).toArray();
    };

    return {
        initializeBlocks: initializeBlocks
    };
});
