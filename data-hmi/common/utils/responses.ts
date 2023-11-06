import * as express from "express"
import {default as log4js} from "log4js"

const LOGGER = log4js.getLogger();

export function sendJsonResponse(res: express.Response, element: object, status?: number) {
    if (status === undefined) {
        res.status(200);
    } else {
        res.status(status);
    }

    res.setHeader("Content-Type", "application/json");
    res.json(element);
};


export function sendJsonError(res: express.Response, error: object|string, status?: number) {
    let m = error;
    if (m == undefined) {
        m = "Internal server error."
    }
    if (status === undefined) {
        res.status(500);
    } else {
        res.status(status);
    }
    
    res.setHeader("Content-Type", "application/json");

    if (typeof m === 'string' || m instanceof String){
        LOGGER.error(m)
        res.json({
            msg: m
        });
    } else {
        LOGGER.error(JSON.stringify(m))
        res.json(m);
    }
};

export function handleMongooseError(res: express.Response, error: Error) {

    if (error.name != undefined && error.name === "ValidationError") {
        return exports.sendJsonError(res, error.message, 400);
    }

    exports.sendJsonError(res, error.message, 500);

}
