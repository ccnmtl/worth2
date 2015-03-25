/*
 * To build the WORTH js app, run `r.js -o build.js` from the root directory.
 *
 * If r.js isn't available, install it with: `npm install requirejs`.
 */
({
    baseUrl: "./media/js/src",
    mainConfigFile: "./media/js/src/main.js",
    name: "main",
    out: "media/main-built.js"
})
