module.exports = function (req, res, next) {
    res.locals.sse = {};

    res.locals.sse.setup = function () {
        res.writeHead(200, {
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'X-Accel-Buffering': 'no'
        });

        res.locals.sse.timeout = setInterval(() => res.write("\n\n"), 5000);
        res.locals.sse.timeout = setInterval(() => {
            res.write(JSON.stringify({'event': 'reconnect', 'data': ''}));
            res.emit('close');
        }, 20000);
    };

    res.locals.sse.dispose = function () {
        clearInterval(res.locals.sse.timeout)
    };

    res.locals.sse.emit = function (event, data) {
        let notification = {event: event, data: data};
        res.write(JSON.stringify(notification) + "\r\n");
    };

    next()
};