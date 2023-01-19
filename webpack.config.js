const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CopyWebpackPlugin = require("copy-webpack-plugin");

const source = path.resolve(path.join("./wagtail_helpdesk", "./static_src"));
const destination = path.resolve(path.join("./wagtail_helpdesk", "./static", "./wagtail_helpdesk"));

module.exports = (env, argv) => {
  const isProductionMode = argv.mode === "production";

  return {
    entry: {
      main: [
        path.join(source, "js", "main.js"),
        path.join(source, "scss", "main.scss"),
      ],
    },
    output: {
      path: destination,
      publicPath: "/static/wagtail_helpdesk/",
      filename: "[name].js",
      clean: true,
    },
    devtool: isProductionMode ? false : "inline-source-map",
    module: {
      rules: [
        {
          test: /\.js$/,
          exclude: /node_modules/,
          use: {
            loader: "babel-loader",
            options: {
              presets: ["@babel/preset-env"]
            }
          }
        },
        {
          test: /\.(scss|css)$/,
          use: [
            MiniCssExtractPlugin.loader,
            {
              loader: "css-loader",
              options: {
                sourceMap: true,
              },
            },
            {
              loader: "postcss-loader",
              options: {
                sourceMap: true,
                postcssOptions: {
                  plugins: [
                    "postcss-preset-env"
                  ]
                }
              },
            },
            "sass-loader",
          ],
        },
      ],
    },
    plugins: [
      new MiniCssExtractPlugin({
        filename: "[name].css",
      }),
      new CopyWebpackPlugin({
        patterns: [
          {
            from: path.join(source, "images"),
            to: path.join(destination, "images"),
          },
        ],
      }),
    ],
  }
}
