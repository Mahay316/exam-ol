const path = require('path')
const VueLoaderPlugin = require('vue-loader/lib/plugin')

module.exports = {
    mode: "production",
    entry: {
        stat: './src/js/stat.js'
    },
    output: {
        path: path.resolve(__dirname, 'static/dist'),
        filename: '[name].js'
    },
    module: {
        rules: [
            {
                test: /\.vue$/,
                use: 'vue-loader'
            },
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader']
            }
        ]
    },
    plugins: [
        new VueLoaderPlugin()
    ],
    resolve: {
        alias: {'vue$': 'vue/dist/vue.esm.js'},
        extensions: ['.js', '.css', '.vue']
    }
}
