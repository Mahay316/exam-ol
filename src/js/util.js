/**
 * 解析当前页面对应的url中的查询参数
 * @returns 查询参数组成的键值对
 */
export function parseSearchParam() {
    let res = {};
    let params = location.search.substring(1).split('&');
    params.forEach(ele => {
        // 拆分成键值对，放入res对象中
        let pair = ele.split('=');
        res[pair[0]] = pair[1];
    });

    return res;
}
