const Layout = () => import('@/layout/index.vue')

export default {
    path: '/statistics',
    component: Layout,
    redirect: '/statistics/batchactionbar',
    name: 'statistics',
    meta: {
        title: '统计',
        icon: 'sidebar-menu'
    },
    children: [
        {
            path: 'videodata',
            name: 'statistics.videodata',
            component: () => import('@/views/component_extend_example/statistics.batchactionbar.vue'),
            meta: {
                title: '视频数据'
            }
        },
        {
            path: 'userdata',
            name: 'statistics.userdata',
            component: () => import('@/views/component_extend_example/statistics.batchactionbar.vue'),
            meta: {
                title: '用户数据'
            }
        }
    ]
}
