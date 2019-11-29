const webpack = require("webpack");
const resolve = require("path").resolve;

const config = {
  devtool: "eval-source-map",
  entry: __dirname + "/js/index.js",
  output: {
    path: resolve("../public"),
    filename: "bundle.js",
    publicPath: resolve("../public")
  },
  resolve: {
    extensions: [".js", ".css"]
  },
  module: {
    rules: [
      {
        test: /\.js?/,
        loader: "babel-loader",
        exclude: /node_modules/
      },
      {
        test: /\.css$/,
        loader: "style-loader!css-loader?modules"
      }
    ]
  }
};
module.exports = config;
