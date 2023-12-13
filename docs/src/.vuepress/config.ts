import { defaultTheme } from 'vuepress'
const { description } = require('../../package')

export default {
    /**
     * Ref：https://v1.vuepress.vuejs.org/config/#title
     */
    title: 'DicerGirl',
    /**
     * Ref：https://v1.vuepress.vuejs.org/config/#description
     */
    description: description,

    /**
     * Extra tags to be injected to the page HTML `<head>`
     *
     * ref：https://v1.vuepress.vuejs.org/config/#head
     */
    head: [
        ['meta', { name: 'theme-color', content: '#3eaf7c' }],
        ['meta', { name: 'apple-mobile-web-app-capable', content: 'yes' }],
        ['meta', { name: 'apple-mobile-web-app-status-bar-style', content: 'black' }]
    ],

    /**
     * Theme configuration, here is the default theme configuration for VuePress.
     *
     * ref：https://v1.vuepress.vuejs.org/theme/default-theme-config.html
     */
    theme: defaultTheme({
        repo: 'https://github.com/noctisynth/dicer',
        docsDir: 'docs',
        editLinkText: '编辑此页',
        lastUpdated: true,
        navbar: [
            {
                text: '概览',
                link: '/overview/',
            },
        ],
        sidebar: [{
            text: '概览',
            link: '/overview/',
            children: []
        }],
    }),

    /**
     * Apply plugins，ref：https://v1.vuepress.vuejs.org/zh/plugin/
     */
    plugins: [
    ]
}
