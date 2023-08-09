var item1 = document.querySelector('.top');
        var itemPos1 = 0;
        var minPos1 = -0.32 * window.innerHeight;
        var maxPos1 = 0;
        var item2 = document.getElementById('title');
        var itemxPos2 = 0;
        var minxPos2 = -0.4 * window.innerWidth;
        var maxxPos2 = 0;
        var itemyPos2 = 0;
        var minyPos2 = 0;
        var maxyPos2 = 0.16 * window.innerHeight;
        var itemScal2 = 1;
        var minScal2 = 0.3;
        var maxScal2 = 1;
        var item3 = document.getElementById('subtitle');
        var itemPos3 = 0;
        var minPos3 = 0;
        var maxPos3 = 0.8 * window.innerWidth;
        // item2.style.transform = 'translate(-500px, 110px) scale(0.3)';
        function handleScroll(event) {
            // document.getElementById('message').textContent = "scrolling";
            var delta = event.wheelDelta ;//|| -event.deltaY
            // document.getElementById('num0').textContent = currentPos
            // document.getElementById('num1').textContent = delta
            // document.getElementById('num2').textContent = itemPos1
            itemPos1 += delta * (maxPos1 - minPos1) / 400;
            if (itemPos1 < minPos1) itemPos1 = minPos1;
            if (itemPos1 > maxPos1) itemPos1 = maxPos1;
            item1.style.transform = 'translateY(' + itemPos1 + 'px)';

            itemxPos2 += delta * (maxxPos2 - minxPos2) / 400;
            itemyPos2 -= delta * (maxyPos2 - minyPos2) / 400;
            itemScal2 += delta * (maxScal2 - minScal2) / 400;
            if (itemxPos2 < minxPos2) itemxPos2 = minxPos2;
            if (itemxPos2 > maxxPos2) itemxPos2 = maxxPos2;
            if (itemyPos2 < minyPos2) itemyPos2 = minyPos2;
            if (itemyPos2 > maxyPos2) itemyPos2 = maxyPos2;
            if (itemScal2 < minScal2) itemScal2 = minScal2;
            if (itemScal2 > maxScal2) itemScal2 = maxScal2;
            item2.style.transform = 'translate(' + itemxPos2 + 'px, ' + itemyPos2 + 'px) scale(' + itemScal2 + ')';

            itemPos3 -= delta * (maxPos3 - minPos3) / 400;
            if (itemPos3 < minPos3) itemPos3 = minPos3;
            if (itemPos3 > maxPos3) itemPos3 = maxPos3;
            item3.style.transform = 'translateX(' + itemPos3 + 'px)';

            event.preventDefault();
        }

        window.addEventListener('wheel', handleScroll);