/*
  Small mixin for handling a successful donation - controllers using this mixin
  should also include the SaveDonationMixin.
*/
App.DonationSuccessMixin = Em.Mixin.create({
});


App.OrderController = Em.ObjectController.extend();

App.OrderSignupController = App.SignupController.extend(App.SaveDonationMixin, App.DonationSuccessMixin, {
    _handleSignupSuccess: function () {
        // Update the user on the order to the current user
        var _this = this,
            donation = this.get('controllers.donation.model'),
            order = donation.get('order');

        App.UserPreview.find(this.get('currentUser.id_for_ember')).then(function (user) {
            order.set('user', user).send('becomeDirty');
            order.save().then(function (order) {
                // Save the current donation after successful signup
                _this._saveDonation();
            });
        });
    },

    _handleSignupConflict: function (failedUser) {
        var conflict = failedUser.errors.conflict,
            loginObject = App.UserLogin.create({
                matchId: conflict.id,
                matchType: conflict.type,
                email: failedUser.get('email')
            });

        this.send('modalContent', 'orderLogin', loginObject);
    },

    actions: {
        guestPayment: function () {
            this._saveDonation();
        }
    }
});

App.OrderLoginController = App.LoginController.extend(App.SaveDonationMixin, App.DonationSuccessMixin, {
    _handleLoginSuccess: function () {
        // Update the user on the order to the current user
        var _this = this,
            donation = this.get('controllers.donation.model'),
            order = donation.get('order');


        App.UserPreview.find(this.get('currentUser.id_for_ember')).then(function (user) {
            order.set('user', user).send('becomeDirty');
            order.save().then(function (order) {
                // Save the current donation after successful signup
                _this._saveDonation();
            });
        });
    }
});