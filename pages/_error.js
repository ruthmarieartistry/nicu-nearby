import React from "react";

function Error({ statusCode }) {
  return React.createElement(
    "p",
    null,
    statusCode
      ? `An error ${statusCode} occurred on server`
      : "An error occurred on client",
  );
}

Error.getInitialProps = ({ res, err }) => {
  const statusCode = res ? res.statusCode : err ? err.statusCode : 404;
  return { statusCode };
};

export default Error;
