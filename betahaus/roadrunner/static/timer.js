function Timer(display_selector) {
    this.start_timestamp = null;
    this.entry_title = null;
    this.entry_url = null;
    this.display_selector = display_selector;
    this.debug = false;
    this.event_timer = null;

    this.read = function() {
        request = arche.do_request('/timer_controls/read');
        var that = this;
        request.done(function(response) {
            console.log("Read timestamp was: ", response['epoch'])
            that.start_timestamp = response['epoch'];
            that.entry_title = response['title'];
            that.entry_url = response['url'];
            that.ctrlUpdate();
        });
    }
    this.stop = function() {
        request = arche.do_request('/timer_controls/stop');
        var that = this;
        request.done(function(response) {
            console.log("stop timestamp");
            that.start_timestamp = null;
            that.entry_title = null;
            that.entry_url = null;
            that.ctrlUpdate();
        });
        //Stop stuff
    }
    this.start = function(url) {
        if (this.start_timestamp != null) {
            arche.create_flash_message("Timer already running", {type: 'danger', auto_destruct: true});
        } else {
            request = arche.do_request(url);
            var that = this;
            request.done(function(response) {
                console.log("start timestamp: ", response['epoch']);
                that.start_timestamp = response['epoch'];
                that.entry_title = response['title'];
                that.entry_url = response['url'];
                that.ctrlUpdate();
            });
        }
    }

    this.startFromClick = function(event) {
        console.log("Start from click");
        event.preventDefault();
        this.start($(event.currentTarget).attr('href'));
    }

    this.stopFromClick = function(event) {
        console.log("Stop from click");
        event.preventDefault();
        this.stop();
    }

    this.getDiff = function() {
        //console.log("getDiff functions start_timestamp value: ", this.start_timestamp);
        //console.log("Current timestamp: ", Math.floor($.now() / 1000));
        if (this.start_timestamp != null) {
            return Math.floor($.now() / 1000) - this.start_timestamp
        } else {
            return '-'
        }
    }

    this.ctrlUpdate = function() {
        if (this.start_timestamp == null) {
            console.log("Hide stop");
            $('[data-timer-control="stop"]').hide();
            $('[data-timer-slot]').empty();
            $('[data-timer-title]').empty();
            $('[data-timer-title]').attr('href', '');
        } else {
            console.log("Show stop");
            $('[data-timer-control="stop"]').show();
        }
    }

    this.initEventTimer = function(callback) {
        if (this.event_timer == null) {
            console.log("Init timer");
            var that = this;
            this.event_timer = setInterval(callback, 200);
        }
    }

    this.update = function() {
        if (this.start_timestamp != null) {
            $('[data-timer-slot]').html(this.getDiff());
            $('[data-timer-title]').html(this.entry_title);
            $('[data-timer-title]').attr('href', this.entry_url);
        }
    }

}

var timer = new Timer();

function delegate_event_timer(arg) {
    timer.update()
}

function update_from_json(event) {
    var $button = $(event.currentTarget);
    var $container = $button.closest('[data-update-container]');
    $button.addClass('updating');
    $.get($button.data('updateJson'))
    .done(function(data) {
        $.each(data.updated_fields, function(key, value) {
            $container.find('[data-update-name="' + key + '"]').text(value);
        });
    })
    .fail(function() {
        alert('Update failed');
    })
    .always(function() {
        $button.removeClass('updating');
        $button.blur();
    });
}

$(document).ready(function () {
    timer.read();
    timer.initEventTimer(delegate_event_timer);
    //FIXME: Narrow down selectors?
    $('body').on('click', '[data-add-task-timer]', function(event) {
        timer.startFromClick(event);
    });
    $('body').on('click', '[data-timer-control="stop"]', function(event) {
        timer.stopFromClick(event);
    });
    $('[data-update-json]').click(update_from_json);
});
