import logging

from colorama import Fore
from GramAddict.core.views import (
    HashTagView,
    PlacesView,
    PostsGridView,
    ProfileView,
    TabBarView,
)
from GramAddict.core.utils import random_sleep

logger = logging.getLogger(__name__)


def check_if_english(device):
    pass
    # logger.info("Switching to English locale", extra={"color": f"{Fore.GREEN}"})
    # profile_view = TabBarView(device).navigateToProfile()
    # logger.info("Changing language in settings")

    # options_view = profile_view.navigateToOptions()
    # settingts_view = options_view.navigateToSettings()
    # account_view = settingts_view.navigateToAccount()
    # language_view = account_view.navigateToLanguage()
    # language_view.setLanguage("english")


def nav_to_blogger(device, username, current_job):
    """navigate to blogger (followers list or posts)"""
    _to_followers = True if current_job.endswith("followers") else False
    if username is None:
        logger.info("Open your followers")
        profile_view = TabBarView(device).navigateToProfile()
        if _to_followers:
            profile_view.navigateToFollowers()
    else:
        search_view = TabBarView(device).navigateToSearch()
        profile_view = search_view.navigateToUsername(username)
        random_sleep()
        if not profile_view:
            return False

        logger.info(f"Open @{username} followers")
        if _to_followers:
            profile_view.navigateToFollowers()
    return True


def nav_to_hashtag_or_place(device, target, current_job):
    """navigate to hashtag/place list"""
    search_view = TabBarView(device).navigateToSearch()
    if (
        not search_view.navigateToHashtag(target)
        if current_job.startswith("hashtag")
        else not search_view.navigateToPlaces(target)
    ):
        return False

    TargetView = HashTagView if current_job.startswith("hashtag") else PlacesView

    if current_job.endswith("recent"):
        logger.info("Switching to Recent tab")
        TargetView(device)._getRecentTab().click()

        random_sleep()
        if TargetView(device)._check_if_no_posts():
            TargetView(device)._reload_page()
            random_sleep()

    logger.info("Opening the first result.")

    result_view = TargetView(device)._getRecyclerView()
    TargetView(device)._getFistImageView(result_view).click()
    random_sleep()
    return True


def nav_to_post_likers(device, username, my_username):
    """navigate to blogger post likers"""
    if username == my_username:
        TabBarView(device).navigateToProfile()
    else:
        search_view = TabBarView(device).navigateToSearch()
        if not search_view.navigateToUsername(username):
            return False
    random_sleep()
    profile_view = ProfileView(device)
    is_private = profile_view.isPrivateAccount()
    posts_count = profile_view.getPostsCount()
    is_empty = posts_count == 0
    if is_private or is_empty:
        private_empty = "Private" if is_private else "Empty"
        logger.info(f"{private_empty} account.", extra={"color": f"{Fore.GREEN}"})
        return False
    logger.info("Opening the first post")
    ProfileView(device).swipe_to_fit_posts()
    PostsGridView(device).navigateToPost(0, 0)
    random_sleep()
    return True


def nav_to_usernames(device):
    pass
