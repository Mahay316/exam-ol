$(function () {
    // 侧边栏跟随
    const topPadding = 15;
    const headerHeight = 62;
    const sidebar = $("#sidebar");
    const offset = sidebar.offset();
    const container = $('#main');

    if (sidebar.length > 0) {
        $(window).scroll(function () {
            const sideBarHeight = sidebar.height();
            if ($(window).scrollTop() + headerHeight > offset.top) {
                let newPosition = $(window).scrollTop() + headerHeight - offset.top + topPadding;
                const maxPosition = container.height() - sideBarHeight - 2;
                if (newPosition > maxPosition) {
                    newPosition = maxPosition;
                }
                sidebar.stop().animate({
                    marginTop: newPosition
                });
            } else {
                sidebar.stop().animate({
                    marginTop: 0
                });
            }
        });
    }
});
