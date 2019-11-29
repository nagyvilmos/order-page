import { request, reply } from "./action";

const checkJson = (checkJsonFunction, json) =>
  json === undefined
    ? false
    : checkJsonFunction === undefined
    ? true
    : checkJsonFunction(json);

function log(name, detail) {
  if (name === undefined) {
    return;
  }
  console.log({ [name]: detail });
}

export function dispatchUri(
  uri,
  content,
  pendingAction,
  checkJsonFunction,
  successActionFunction,
  failureActionFunction,
  errorActionFunction,
  logName
) {
  return dispatch => {
    log(logName, uri);
    if (pendingAction) {
      dispatch(pendingAction);
    }
    fetch(uri, content)
      .then(res => {
        log(logName, { res });
        if (res.ok) {
          return res.json();
        }
        console.warn("dispatchUri.status " + res.status + ":" + res.statusText);
        if (res.status === 401) {
          dispatch(logout());
        }
        Promise.reject(res.statusText);
      })
      .catch(error => {
        log(logName, { error });
        if (errorActionFunction) {
          dispatch(errorActionFunction(error));
        }
      })
      .then(json => {
        const success = checkJson(checkJsonFunction, json);
        log(logName, { json, success });
        if (success) {
          log(logName, "success");
          if (successActionFunction) {
            dispatch(successActionFunction(json));
          }
        } else {
          log(logName, "failure");
          if (failureActionFunction) {
            dispatch(failureActionFunction(json));
          }
        }
      })
      .catch(error => {
        log(logName, { error });
        if (errorActionFunction) {
          dispatch(errorActionFunction(error));
        }
      });
  };
}

/**
 * Dispatch a request to get the json from an uri
 * @param {string} uri
 *  specifies the uri to request
 * @param {string} authToken
 *  authorisatin token for the call
 *  if undefined then no authorisation is provided
 * @param {action} pendingAction
 *  action to dispatch before making the call
 *  if undefined then no action is dispatched
 * @param {function} checkJsonFunction
 *  function that takes the json and returns true/false to indicate if the data is okay,
 *  if undefined then json is okay if it exists
 * @param {function} successActionFunction
 *  function that takes the json and returns an action to be dispatched when the json is okay
 *  if undefined then no action is dispatched
 * @param {function} failureActionFunction
 *  function that takes the json and returns an action to be dispatched when the json is not okay
 *  if undefined then no action is dispatched
 * @param {function} errorActionFunction
 *  function that takes an error returns an action to be dispatched when one is caught
 *  if undefined then no action is dispatched
 * @param {string} logName
 *  if set, the steps of the call are logged with this name.
 *  this argument should not be used in production code
 */
export function getUri(
  uri,
  authToken,
  pendingAction,
  checkJsonFunction,
  successActionFunction,
  failureActionFunction,
  errorActionFunction,
  logName
) {
  const headers =
    authToken === undefined
      ? {
          "Content-Type": "application/json"
        }
      : {
          "Content-Type": "application/json",
          Authorization: "Bearer " + authToken
        };
  return dispatchUri(
    uri,
    { headers: headers },
    pendingAction,
    checkJsonFunction,
    successActionFunction,
    failureActionFunction,
    errorActionFunction,
    logName
  );
}

/**
 * Dispatch a request to post json to an uri
 * @param {string} uri
 *  specifies the uri to request
 * @param {json} payload
 *  the json payload to be sent
 * @param {string} authToken
 *  authorisatin token for the call
 *  if undefined then no authorisation is provided
 * @param {action} pendingAction
 *  action to dispatch before making the call
 *  if undefined then no action is dispatched
 * @param {function} checkJsonFunction
 *  function that takes the json and returns true/false to indicate if the data is okay,
 *  if undefined then json is okay if it exists
 * @param {function} successActionFunction
 *  function that takes the json and returns an action to be dispatched when the json is okay
 *  if undefined then no action is dispatched
 * @param {function} failureActionFunction
 *  function that takes the json and returns an action to be dispatched when the json is not okay
 *  if undefined then no action is dispatched
 * @param {function} errorActionFunction
 *  function that takes an error returns an action to be dispatched when one is caught
 *  if undefined then no action is dispatched
 * @param {string} logName
 *  if set, the steps of the call are logged with this name.
 *  this argument should not be used in production code
 */
export function postUri(
  uri,
  payload,
  authToken,
  pendingAction,
  checkJsonFunction,
  successActionFunction,
  failureActionFunction,
  errorActionFunction,
  logName
) {
  const headers =
    authToken === undefined
      ? {
          Accept: "application/json, text/plain, */*",
          "Content-Type": "application/json"
        }
      : {
          Accept: "application/json, text/plain, */*",
          "Content-Type": "application/json",
          Authorization: "Bearer " + authToken
        };
  const constent = {
    headers: headers,
    method: "post",
    body: JSON.stringify(payload)
  };

  return dispatchUri(
    uri,
    constent,
    pendingAction,
    checkJsonFunction,
    successActionFunction,
    failureActionFunction,
    errorActionFunction,
    logName
  );
}

export function getData(requestData) {
  return postUri("api", requestData, (logName = "getData"));
}
