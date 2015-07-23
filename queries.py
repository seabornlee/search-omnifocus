from __future__ import unicode_literals

TASK_SELECT = ("t.persistentIdentifier, t.name, t.dateCompleted, "
               "t.blocked, c.name, p.name, t.flagged, t.dateToStart, "
               "t.inInbox, t.effectiveInInbox, t.effectiveDateToStart ")
TASK_FROM = ("((task tt left join projectinfo pi on tt.containingprojectinfo=pi.pk) t left join "
             "task p on t.task=p.persistentIdentifier) left join "
             "context c on t.context = c.persistentIdentifier")
TASK_NAME_WHERE = "lower(t.name) LIKE lower('%{0}%')"
ACTIVE_CLAUSE = "t.blocked = 0 AND "


def search_tasks(active_only, query):
    stm_where = ("t.childrenCountAvailable = 0 AND "
                 "(t.effectiveInInbox = 0 AND t.inInbox = 0) AND "
                 "t.dateCompleted IS NULL AND ")
    stm_where = (stm_where + TASK_NAME_WHERE).format(query)
    stm_ignore_projects = "t.containingProjectInfo <> t.persistentIdentifier"

    if active_only:
        stm_where = ("t.blocked = 0 AND " + stm_where)

    return "SELECT {0} FROM {1} WHERE {2} AND {3}".format(TASK_SELECT, TASK_FROM, stm_where, stm_ignore_projects)


def search_inbox(query):
    stm_where = ("(t.effectiveInInbox = 1 OR t.inInbox = 1) AND "
                 "t.dateCompleted IS NULL AND ")
    stm_where = (stm_where + TASK_NAME_WHERE).format(query)
    return "SELECT {0} FROM {1} WHERE {2}".format(TASK_SELECT, TASK_FROM, stm_where)


def search_projects(active_only, query):
    stm_select = ("p.pk, t.name, p.status, p.numberOfAvailableTasks, "
                  "p.numberOfRemainingTasks, p.containsSingletonActions, f.name, t.dateToStart, t.effectiveDateToStart")
    stm_from = ("(ProjectInfo p LEFT JOIN Task t ON p.task=t.persistentIdentifier) "
                "LEFT JOIN Folder f ON p.folder=f.persistentIdentifier")
    stm_where = "lower(t.name) LIKE lower('%{0}%')".format(query)
    stm_order = "p.containsSingletonActions DESC, t.name ASC"

    if active_only:
        stm_where = ("p.status = 'active' AND " + stm_where)

    return "SELECT {0} FROM {1} WHERE {2} ORDER BY {3}".format(stm_select, stm_from, stm_where, stm_order)


def search_contexts(query):
    stm_select = "persistentIdentifier, name, allowsNextAction, active, availableTaskCount"
    stm_from = "Context"
    stm_where = "active = 1 AND lower(name) LIKE lower('%{0}%')".format(query)
    stm_order = "name ASC"

    return "SELECT {0} FROM {1} WHERE {2} ORDER BY {3}".format(stm_select, stm_from, stm_where, stm_order)
